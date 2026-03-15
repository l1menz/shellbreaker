# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Build-time env: set via Railway or build arg
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

# Serve stage - use serve (respects Railway's PORT)
FROM node:20-alpine

RUN npm install -g serve

COPY --from=builder /app/dist /app/dist

WORKDIR /app/dist

# Railway injects PORT; default 3000 for local
ENV PORT=3000
EXPOSE 3000

CMD ["sh", "-c", "serve -s . -l ${PORT:-3000}"]
