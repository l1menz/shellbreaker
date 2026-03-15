const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const TOKEN_KEY = 'shellbreaker_token';

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

async function request(path, options = {}) {
  const url = `${API_BASE_URL}${path}`;
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  const res = await fetch(url, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(text || `Request failed with ${res.status}`);
  }

  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    return res.json();
  }
  return res.text();
}

// ——— Auth ———
export function login(username, password) {
  const body = new URLSearchParams({ username, password });
  return fetch(`${API_BASE_URL}/users/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  }).then(async (res) => {
    if (!res.ok) {
      const text = await res.text().catch(() => '');
      throw new Error(text || `Login failed: ${res.status}`);
    }
    return res.json();
  });
}

export function register({ username, email, password }) {
  return request('/users/register', {
    method: 'POST',
    body: JSON.stringify({ username, email, password }),
  });
}

export function getMe() {
  return request('/users/me');
}

// ——— Leaderboard (no auth) ———
export function getLeaderboard(limit = 10) {
  return request(`/users/leaderboard?limit=${limit}`);
}

// ——— Challenges ———
export function getChallenges() {
  return request('/challenges/');
}

export function getChallenge(id) {
  return request(`/challenges/${id}`);
}

// ——— Progress (today’s tasks, complete, history) ———
export function getTodayChallenges() {
  return request('/progress/today');
}

export function completeChallenge(userChallengeId) {
  return request('/progress/complete', {
    method: 'POST',
    body: JSON.stringify({ user_challenge_id: userChallengeId }),
  });
}

export function getProgressHistory() {
  return request('/progress/history');
}

// ——— NFC scan (assign tag's challenges to user) ———
export function nfcScanTag(tagType) {
  return request('/nfc/scan', {
    method: 'POST',
    body: JSON.stringify({ tag_type: tagType }),
  });
}
