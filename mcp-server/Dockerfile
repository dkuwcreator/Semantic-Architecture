FROM node:20-alpine AS build
WORKDIR /app
COPY mcp-server/package.json mcp-server/package-lock.json* ./
RUN npm ci
COPY mcp-server/ .
RUN npm run build
RUN npm prune --production

FROM node:20-alpine
WORKDIR /srv
ENV NODE_ENV=production
COPY --from=build /app/package.json ./package.json
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
# Copy repo root into container at /workspace so tools can read your docs & modules
COPY . /workspace
ENV REPO_ROOT=/workspace
EXPOSE 3000
ENTRYPOINT ["node", "dist/server.js"]
CMD ["--stdio"]
