# Stage 1: Build the React frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Stage 2: Backend & Runtime
FROM node:20-alpine AS runner
WORKDIR /app

# Install openssl, libc6-compat, and python3 for youtube-dl-exec and Prisma runtime
RUN apk add --no-cache openssl libc6-compat python3
ENV YOUTUBE_DL_SKIP_PYTHON_CHECK=1

# Install backend dependencies
COPY backend/package*.json ./backend/
WORKDIR /app/backend
RUN npm ci

# Copy backend source & Prisma schema
COPY backend/ ./

# Generate Prisma client for Linux
RUN npx prisma generate

# Copy built frontend assets
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Create uploads folder for local files
RUN mkdir -p /app/backend/uploads

EXPOSE 3001

ENV PORT=3001
ENV NODE_ENV=production
ENV FRONTEND_DIST=/app/frontend/dist
ENV DATABASE_URL="file:./dev.db"

# Sync SQLite database schema and launch server
CMD ["sh", "-c", "npx prisma db push --skip-generate && npx tsx src/server.ts"]
