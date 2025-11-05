FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev

FROM node:20-alpine AS build
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM node:20-alpine
WORKDIR /srv
ENV NODE_ENV=production
COPY --from=build /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
# Copy repo root into container at /workspace so tools can read your docs & modules
# At runtime, you can mount a workspace volume instead; default to image content.
COPY .. /workspace
ENV REPO_ROOT=/workspace
EXPOSE 3000
CMD ["node", "dist/server.js"]
