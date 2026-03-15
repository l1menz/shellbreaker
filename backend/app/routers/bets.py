from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timezone

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/bets", tags=["bets"])

MIN_WAGER = 5


@router.post("/", response_model=schemas.BetOut, status_code=201)
def create_bet(
    body: schemas.BetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Challenge a friend to a bet on a specific challenge.
    Both parties wager the same number of coins. Winner takes the pot.
    Coins are escrowed immediately from the challenger.
    """
    if body.wager < MIN_WAGER:
        raise HTTPException(status_code=400, detail=f"Minimum wager is {MIN_WAGER} coins.")
    if current_user.coins < body.wager:
        raise HTTPException(status_code=400, detail="Insufficient coins.")

    opponent = db.query(models.User).filter(models.User.username == body.opponent_username).first()
    if not opponent:
        raise HTTPException(status_code=404, detail="Opponent not found.")
    if opponent.id == current_user.id:
        raise HTTPException(status_code=400, detail="You can't bet against yourself.")

    challenge = db.query(models.Challenge).filter(models.Challenge.id == body.challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found.")

    # Escrow challenger's coins
    current_user.coins -= body.wager

    bet = models.Bet(
        challenger_id=current_user.id,
        opponent_id=opponent.id,
        challenge_id=body.challenge_id,
        wager=body.wager,
    )
    db.add(bet)
    db.commit()
    db.refresh(bet)
    return bet


@router.get("/", response_model=list[schemas.BetOut])
def list_my_bets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """All bets the current user is involved in."""
    return (
        db.query(models.Bet)
        .filter(
            or_(
                models.Bet.challenger_id == current_user.id,
                models.Bet.opponent_id == current_user.id,
            )
        )
        .order_by(models.Bet.created_at.desc())
        .all()
    )


@router.post("/respond", response_model=schemas.BetOut)
def respond_to_bet(
    body: schemas.BetAction,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Accept or decline an incoming bet.
    Accepting escrows the opponent's coins and makes the bet active.
    Declining refunds the challenger's coins.
    """
    if body.action not in ("accept", "decline"):
        raise HTTPException(status_code=400, detail="action must be 'accept' or 'decline'.")

    bet = (
        db.query(models.Bet)
        .filter(
            models.Bet.id == body.bet_id,
            models.Bet.opponent_id == current_user.id,
            models.Bet.status == models.BetStatus.open,
        )
        .first()
    )
    if not bet:
        raise HTTPException(status_code=404, detail="Open bet not found.")

    if body.action == "decline":
        # Refund challenger
        bet.challenger.coins += bet.wager
        bet.status = models.BetStatus.cancelled

    else:
        # Accept: escrow opponent's coins
        if current_user.coins < bet.wager:
            raise HTTPException(status_code=400, detail="Insufficient coins to accept this bet.")
        current_user.coins -= bet.wager
        bet.status = models.BetStatus.active

    db.commit()
    db.refresh(bet)
    return bet


@router.post("/{bet_id}/complete", response_model=schemas.BetOut)
def complete_bet(
    bet_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Called when the current user completes the challenge tied to an active bet.
    First to complete wins. Winner receives the full pot (2x wager).
    """
    bet = (
        db.query(models.Bet)
        .filter(
            models.Bet.id == bet_id,
            models.Bet.status == models.BetStatus.active,
            or_(
                models.Bet.challenger_id == current_user.id,
                models.Bet.opponent_id == current_user.id,
            ),
        )
        .first()
    )
    if not bet:
        raise HTTPException(status_code=404, detail="Active bet not found.")

    # Award pot to winner
    current_user.coins += bet.wager * 2
    bet.winner_id = current_user.id
    bet.status = models.BetStatus.completed
    bet.resolved_at = datetime.now(timezone.utc)

    # Also mark the challenge complete for this user if not already done
    uc = (
        db.query(models.UserChallengeProgress)
        .filter(
            models.UserChallengeProgress.user_id == current_user.id,
            models.UserChallengeProgress.challenge_id == bet.challenge_id,
            models.UserChallengeProgress.status != models.ChallengeStatus.completed,
        )
        .first()
    )
    if uc:
        uc.status = models.ChallengeStatus.completed
        uc.completed_at = datetime.now(timezone.utc)
        current_user.xp += bet.challenge.xp_reward

    db.commit()
    db.refresh(bet)
    return bet