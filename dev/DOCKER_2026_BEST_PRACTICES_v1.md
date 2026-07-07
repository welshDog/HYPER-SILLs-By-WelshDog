# HS-137 — 🐳 DOCKER SOVEREIGN — Docker 2026 Best Practices (Production Dockerfiles)

---
skill_id: HS-137
hero_name: "DOCKER SOVEREIGN"
emoji: "🐳"
version: v1.0.0
status: ACTIVE
category: dev
depends_on:
  - HS-060  # FLEET ADMIRAL — Container Stack Reference
  - HS-114  # BRAIN OPS — Hyper Brain Infrastructure Runbook
  - HS-136  # AGENT SCRIBE — Docker Agent YAML Declaration Pattern
provides:
  - multi-stage-buildkit-dockerfile
  - production-docker-image-pattern
  - non-root-container-security
  - dumb-init-signal-handling
  - docker-healthcheck-pattern
  - nextjs-standalone-build
  - express-vite-spa-container
  - alpine-minimal-runtime
  - dockerignore-template
  - npm-ci-reproducible-install
related:
  - HS-060  # FLEET ADMIRAL — Container Stack Reference
  - HS-061  # THE PORT WARDEN — Port + Network Map
  - HS-135  # GATEWAY SOVEREIGN — Docker MCP Toolkit
  - HS-136  # AGENT SCRIBE — Docker Agent YAML Pattern
graph_notes: "2026 production-ready Dockerfile pattern for Node 20 apps. Multi-stage BuildKit, non-root (UID 1001), dumb-init PID 1, HEALTHCHECK, Alpine runtime. Mission Control Express+Vite landed 74.2MB. Home Page Next.js standalone targets ~140MB. Security-by-default, orchestrator-ready."
problem_keywords:
  - docker production dockerfile
  - multi-stage build
  - node alpine docker
  - non-root docker container
  - docker healthcheck
  - nextjs standalone docker
  - express vite docker
  - buildkit optimization
  - docker image size
  - dumb-init signal handling
  - npm ci docker
  - docker security best practices
  - 2026 docker pattern

---

**Category:** `dev/`
**Version:** v1.0.0
**Born from:** Mission Control (Express + Vite SPA) + Home Page (Next.js) production deployments — July 2026
**Replaces the pain of:** bloated node:20 images (1.2GB), root-running containers, no signal handling, floating npm installs, zero health visibility for orchestrators.

---

## 🐳 What It Does

**One pattern. Production-ready. Secure by default. Orchestrator-aware.**

Takes a Node.js app (Express API + Vite SPA, or Next.js) and produces a minimal, hardened, production Docker image using 2026 best practices — multi-stage BuildKit, Alpine runtime, non-root user, dumb-init PID 1, HEALTHCHECK, and npm ci lockfile installs.

**Results from Mission Control:**
- Image size: **74.2MB** (vs ~1.2GB with node:20 + dev deps)
- Base: `node:20-alpine` = 174MB vs `node:20` = 1.2GB — **86% smaller**
- Runtime: Express server + prebuilt Vite SPA dist/ only — zero build tooling in production

---

## 🎯 When To Use

- Deploying any Node.js app (API, SPA, Next.js, Express) to containers
- Want smaller images, reproducible builds, and hardened runtime security
- Using orchestrators (Kubernetes, Docker Compose, Render) that rely on HEALTHCHECK for restarts/readiness
- Migrating from node:20 fat images to minimal Alpine/distroless runtimes
- Setting up CI/CD pipelines that need fast, cache-optimised Docker builds

---

## 🔑 The Five Pillars (2026 Standards)

| Pillar | What It Means | Why It Matters |
|---|---|---|
| **Multi-stage builds** | Build in builder stage, copy only artifacts to runtime | Strips 400+ dev packages from production |
| **Security-first** | Non-root UID 1001, dumb-init PID 1 | No root escalation, proper signal handling |
| **Health checks** | HEALTHCHECK on every image | Orchestrators auto-restart on failure |
| **Cache optimisation** | Deps layer before source copy | CI rebuilds in seconds not minutes |
| **Environment-aware** | All config via env vars | No hardcoded secrets, 12-factor compliant |

---

## 🚀 Mission Control — Express + Vite SPA Dockerfile

**Outcome:** ~74.2MB production image — Express API server + prebuilt Vite SPA assets

```dockerfile
# syntax=docker/dockerfile:1.5
# Stage 1: Builder — install all deps + build frontend + compile server
FROM node:20-alpine AS builder
WORKDIR /app

# Copy lockfiles first — maximise layer cache (only invalidated when deps change)
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build:client   # Vite SPA → dist/
RUN npm run build:server   # TypeScript server → server/dist/

# Stage 2: Runtime — minimal production image only
FROM node:20-alpine AS runtime

# dumb-init: proper PID 1 signal handling (graceful shutdown, no zombie processes)
RUN apk add --no-cache dumb-init

# Non-root user — no root escalation risk
RUN addgroup -S nodejs && adduser -S nodejs -G nodejs -u 1001

WORKDIR /app

# Copy ONLY production artifacts from builder
COPY --from=builder /app/server/dist ./server/dist
COPY --from=builder /app/dist ./dist
COPY package*.json ./

# Install production deps only — strips ~400 dev packages
RUN npm ci --omit=dev

# Switch to non-root user
USER 1001:1001

ENV PORT=3011
EXPOSE 3011

# Orchestrator health check — /api/health must return 200 (unauthenticated)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3011/api/health || exit 1

# dumb-init as entrypoint ensures proper signal forwarding to Node
ENTRYPOINT ["/sbin/dumb-init", "--"]
CMD ["node", "server/dist/index.js"]
```

### Express Health Endpoint (required for HEALTHCHECK)

```typescript
// Add to your Express app — unauthenticated, lightweight
app.get('/api/health', (_req, res) => {
  res.status(200).json({ status: 'ok', ts: Date.now() });
});
```

---

## 🏠 Home Page — Next.js Standalone Dockerfile

**Outcome:** ~140MB production image — standalone Next.js runtime, no build tooling

**Prerequisite — next.config.js:**
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',  // Next.js 13+ — produces self-contained server bundle
};
module.exports = nextConfig;
```

```dockerfile
# syntax=docker/dockerfile:1.5
# Stage 1: Builder
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build
# Next.js outputs: .next/standalone/ + .next/static/

# Stage 2: Runtime
FROM node:20-alpine AS runtime

RUN apk add --no-cache dumb-init
RUN addgroup -S nodejs && adduser -S nodejs -G nodejs -u 1001

WORKDIR /app

# Standalone output contains everything needed — no node_modules required
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

USER 1001:1001

ENV NODE_ENV=production
ENV PORT=3000
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD wget -qO- http://localhost:3000/ || exit 1

ENTRYPOINT ["/sbin/dumb-init", "--"]
CMD ["node", "server.js"]
```

---

## 🛡️ .dockerignore Template

Exclude everything that doesn't belong in a production image:

```
# Dependencies (reinstalled via npm ci in Docker)
node_modules
.npm

# Build outputs (rebuilt in Docker builder stage)
dist
.next
out

# Dev tooling
.vscode
.idea
*.log

# Git history (not needed in image)
.git
.gitignore
.gitattributes

# Test suites (not needed in production)
tests
__tests__
*.test.ts
*.spec.ts
coverage

# Environment files (inject via env vars at runtime)
.env
.env.local
.env.development
.env.production

# Documentation
README.md
docs

# CI/Dev Dockerfiles
Dockerfile.dev
docker-compose.dev.yml
```

---

## 🔒 Security Checklist

- [ ] Non-root runtime user (UID 1001) — `adduser -u 1001`
- [ ] `dumb-init` or `tini` as PID 1 — graceful shutdown
- [ ] `npm ci --omit=dev` in production stage — no dev deps
- [ ] `.dockerignore` excludes `.env`, `node_modules`, `.git`, tests
- [ ] `HEALTHCHECK` defined — orchestrators can detect unhealthy containers
- [ ] No secrets hardcoded — all config via env vars (`ENV PORT`, `ARG`, etc.)
- [ ] Run Docker Scout (or Trivy/Snyk) in CI for CVE scanning
- [ ] Use `node:20-alpine` not `node:20` — 86% smaller base

---

## 📊 Size Comparison

| Image | Size | Notes |
|---|---|---|
| `node:20` | ~1.2GB | Full Debian — do not use in production |
| `node:20-alpine` | ~174MB | Minimal Alpine base — use this |
| Mission Control (Express+Vite) | **74.2MB** | Multi-stage + omit=dev + Alpine |
| Home Page (Next.js standalone) | **~140MB** | Standalone output + Alpine |

---

## ⚡ BuildKit + Cache Tips

```bash
# Enable BuildKit (default in Docker 23+, explicit for older)
export DOCKER_BUILDKIT=1

# Build with cache
docker buildx build --tag mission-control:latest .

# CI cache-from / cache-to (GitHub Actions example)
docker buildx build \
  --cache-from type=gha \
  --cache-to type=gha,mode=max \
  --tag mission-control:latest .
```

**Layer cache order — always deps before source:**
```dockerfile
COPY package*.json ./   # ← only invalidated when deps change
RUN npm ci              # ← cached unless package*.json changed
COPY . .                # ← source changes don't bust dep cache
RUN npm run build       # ← only reruns when source changes
```

---

## 🚢 Build + Run Commands

```bash
# Build Mission Control
docker build -t mission-control:latest .

# Run locally (test production image)
docker run -p 3011:3011 \
  -e PORT=3011 \
  -e NODE_ENV=production \
  -e API_CORS_ORIGINS=http://localhost:3000 \
  mission-control:latest

# Check health
curl http://localhost:3011/api/health

# Build Home Page
docker build -t home-page:latest .

# Run Home Page
docker run -p 3000:3000 \
  -e PORT=3000 \
  -e NODE_ENV=production \
  home-page:latest

# Inspect final image size
docker images | grep -E "mission-control|home-page"

# Push to registry
docker tag mission-control:latest ghcr.io/welshdog/mission-control:latest
docker push ghcr.io/welshdog/mission-control:latest
```

---

## 🔄 Commit These Files (per repo)

Before the Docker build context is clean, ensure these are committed:

```bash
# Mission Control
git add Dockerfile .dockerignore
git commit -m "feat: production Dockerfile — multi-stage BuildKit, non-root, healthcheck"
git push

# Home Page — fix uncommitted files first
git add lib/admin.ts lib/blog.ts components/admin/AgentsLab.tsx
git add Dockerfile .dockerignore next.config.js
git commit -m "feat: Next.js standalone output + production Dockerfile"
git push
```

---

## 🌍 Deploy Targets

| Platform | Approach | Notes |
|---|---|---|
| **Render** | Docker image deploy | Point to `Dockerfile`, set env vars in dashboard |
| **Vercel** | Next.js source deploy | Vercel handles build internally — standalone optional |
| **Kubernetes** | Image + HEALTHCHECK | Use `livenessProbe` + `readinessProbe` pointing to `/api/health` |
| **Docker Compose** | `image:` + `healthcheck:` | Local dev stack or VPS self-host |

---

## 📚 Related Skills

- **HS-060 FLEET ADMIRAL** — Container Stack Reference (port map, service layout)
- **HS-061 THE PORT WARDEN** — Port + Network Map
- **HS-114 BRAIN OPS** — Hyper Brain Infrastructure Runbook (Docker debug steps)
- **HS-135 GATEWAY SOVEREIGN** — Docker MCP Toolkit Profile + Claude Code Wiring
- **HS-136 AGENT SCRIBE** — Docker Agent YAML Declaration Pattern
