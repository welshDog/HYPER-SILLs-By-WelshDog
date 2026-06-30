# HS-130 — 🚢 OCI SKILL SHIP — Distribute Skills as OCI Artifacts

---
skill_id: HS-130
hero_name: "OCI SKILL SHIP"
emoji: "🚢"
version: v1.0.0
status: ACTIVE
category: dev
depends_on:
  - HS-128  # PLUGIN FORGE — produces the exported skill bundle you ship
provides:
  - oci-artifact-skill-distribution
  - versioned-signed-skills
  - registry-agnostic-publishing
related:
  - HS-129  # SKILLS-OVER-MCP — runtime discovery, complements OCI distribution
  - DS-005  # THE GATEKEEPER — gate publishing behind passing checks
graph_notes: "Packages exported Agent Skills as OCI artifacts pushed to any OCI registry (ghcr.io, Docker Hub, Harbor, Zot) for versioned, immutable, signable distribution — the same plumbing as container images."
problem_keywords:
  - oci artifact
  - distribute skills
  - signed skills
  - registry publish

---
**Category:** `dev/`
**Source:** Born-here — skills-oci (salaboy), thomasvitale.com Agent-Skills-as-OCI (2026)
**Version:** v1

---

## 🤔 What It Does

OCI registries aren't just for container images — Helm charts, WASM modules, and
policy bundles already ship as OCI artifacts. Agent Skills now do too. This skill
packages your exported skills and pushes them to **any** OCI registry with `oras`,
giving you versioned, immutable, content-addressed, signable skill releases that
pull anywhere that speaks OCI.

---

## 🎯 Purpose

- **Who uses it:** Teams who need provenance, integrity, and enterprise distribution.
- **When to use it:** On every release tag, after the linter and exporter pass.
- **What it unlocks:** `oras pull ghcr.io/<owner>/<skills>:<tag>` from any registry.

---

## 📥 Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `skills_dir` | `path` | ✅ | Exported Agent Skills (e.g. `dist/agent-skills`) |
| `registry` | `string` | ✅ | `ghcr.io`, `docker.io`, `harbor.example.com`, ... |
| `tag` | `string` | ✅ | Semver release tag |

---

## 📤 Output Format

```bash
oras push ghcr.io/<owner>/hyper-skills:<tag> \
  --artifact-type application/vnd.agentskills.bundle.v1+json \
  <files...>
```

---

## 🔮 Prompt Block

```
You are OCI SKILL SHIP. Publish an exported skills directory as an OCI artifact.

Steps:
1. Run the format exporter to produce a clean skills dir (one SKILL.md per skill).
2. In CI (release-triggered), install oras, log in to the registry with the CI token.
3. oras push <registry>/<owner>/<name>:<tag> with artifact-type
   application/vnd.agentskills.bundle.v1+json and every SKILL.md as a layer.
4. Print the pull command. Gate the whole job behind a green linter run.

Rules:
- Registry-agnostic: anything that speaks OCI works (ghcr, Docker Hub, Harbor, Zot).
- Tag with semver; never overwrite an existing immutable tag.
- Don't publish DRAFT/ARCHIVED skills — export filters them first.
```

---

## 💡 Example Usage

```yaml
# .github/workflows/publish-skills.yml (on: release)
- run: python scripts/export_claude_skills.py --format agentskills --out dist/agent-skills
- uses: oras-project/setup-oras@v1
- run: oras push ghcr.io/${{ github.repository_owner }}/hyper-skills:${{ github.event.release.tag_name }} ...
```

---

## 🚨 Anti-patterns

- **Don't reuse a tag** — OCI artifacts should be immutable per version.
- **Don't ship the source vault** — ship the *exported* runtime format.
- **Don't skip the linter gate** — a broken skill in an immutable artifact is forever.

---

## 🔗 Related Skills

- [[HS-128]] PLUGIN FORGE — produces the bundle this ships
- [[HS-129]] SKILLS-OVER-MCP — runtime discovery counterpart
- [[HS-076]] THE GATEKEEPER — pre-publish checks

---

## 📋 THE PROMPT

> Copy this block into any AI session to activate the skill:

```text
Use skill HS-130 [OCI SKILL SHIP]. Add a release-triggered CI job that exports my skills and pushes them as an OCI artifact to ghcr.io via oras, gated behind the linter, and print the pull command.
```
