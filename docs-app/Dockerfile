# ---------- Base (shared) ----------
FROM node:latest AS base
WORKDIR /app
    
# ---------- Deps layer ----------
FROM base AS deps
# Copy the package files only, for better caching
COPY package.json package-lock.json* pnpm-lock.yaml* ./
RUN set -eux; \
    if [ -f pnpm-lock.yaml ]; then \
    corepack enable; \
    corepack prepare pnpm@latest --activate; \
    pnpm install --frozen-lockfile; \
    elif [ -f yarn.lock ]; then \
    corepack enable; \
    corepack prepare yarn@stable --activate; \
    yarn install --frozen-lockfile; \
    elif [ -f package-lock.json ]; then \
    npm ci; \
    else \
    npm i; \
    fi 
    
# ---------- Builder ----------
FROM base AS builder
ENV NODE_ENV=production
ARG NEXT_PUBLIC_ASSET_PREFIX
ENV NEXT_PUBLIC_ASSET_PREFIX=$NEXT_PUBLIC_ASSET_PREFIX
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# If you have build-time public envs, pass them as --build-arg and map to process.env here.
# e.g. ARG NEXT_PUBLIC_API_URL && ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
RUN npm run build
    
# ---------- Runner ----------
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000
# Create non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
    
# Copy the minimal standalone output
# .next/standalone has server.js and node_modules needed at runtime
COPY --from=builder /app/.next/standalone ./
# Static assets
COPY --from=builder /app/.next/static ./.next/static
# Public assets if you have any
COPY --from=builder /app/public ./public
    
USER nextjs
EXPOSE 3000
    
# server.js is produced by `output: 'standalone'`
CMD ["node", "server.js"]    