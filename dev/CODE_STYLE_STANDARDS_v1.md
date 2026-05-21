# HS-084 — 📐 THE STYLE CODEX — Code Style Standards (Python + TS/React)

**Category:** `dev/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §5
**Version:** v1

---

## 🤔 What It Does

The minimum-non-negotiable formatting + structure rules for code written by any HyperCode agent. Backs the lint config — if you stick to these, husky/black/eslint won't bite.

---

## 📁 File Naming

| Surface | Convention | Example |
|---|---|---|
| Python | `lowercase_with_underscores.py` | `execution_service.py` |
| Python tests | `test_feature_name.py` | `test_execution_service.py` |
| TS/React components | `PascalCase.tsx` | `CodeEditor.tsx` |
| TS utils | `camelCase.ts` | `formatError.ts` |
| CSS | `kebab-case.css` | `editor-container.css` |
| YAML/JSON config | `lowercase-with-hyphens.yml` | `docker-compose.yml` |
| Env files | `UPPERCASE_ENV_FILE` | `.env.production` |
| Docs | `UPPERCASE_README.md` or `Title-Case-Guide.md` | `CLAUDE.md` |

---

## 🐍 Python

```python
# Imports: stdlib, third-party, local (each group blank-line-separated)
import asyncio
import os
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
import structlog

from app.services.execution_service import execution_service
from app.schemas.execution import ExecutionResult

# Constants: UPPER_SNAKE_CASE
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Classes: PascalCase
class ExecutionService:
    """Service for executing code."""

    def __init__(self):
        self.logger = structlog.get_logger()

    async def execute(self, source: str) -> ExecutionResult:
        """Execute source code."""
        pass

# Functions: snake_case with type hints + Google-style docstring
async def execute_hypercode(source: str) -> ExecutionResult:
    """
    Execute HyperCode source.

    Args:
        source: HyperCode source code

    Returns:
        ExecutionResult with stdout, stderr, exit_code

    Raises:
        TimeoutError: If execution exceeds timeout
    """
    pass
```

**Hard rules:**
- Type hints on every function signature
- Google-style docstrings (Args / Returns / Raises)
- 4-space indent, never 3, never mixed (sacred rule)
- `from app.X import Y` — never `from backend.app.X` (sacred rule)

---

## ⚛️ TypeScript / React

```typescript
// Imports: React, third-party, local
import React, { useState, useEffect } from 'react';
import { Monaco } from '@monaco-editor/react';

import { ExecutionResult } from './types';
import { formatError } from './utils';

// Types/Interfaces: PascalCase
interface ExecutionResult {
  success: boolean;
  stdout: string;
  stderr: string;
  exitCode: number;
}

// Components: PascalCase, function components, JSX.Element return
export function CodeEditor(): JSX.Element {
  const [code, setCode] = useState<string>('');
  const [result, setResult] = useState<ExecutionResult | null>(null);

  const handleRun = async (): Promise<void> => {
    // ...
  };

  return <div className="editor-container">{/* */}</div>;
}

// Hooks: camelCase with `use` prefix
function useAgentEvents(url: string) {
  const [events, setEvents] = useState<Event[]>([]);
  useEffect(() => {
    const es = new EventSource(url);
    es.onmessage = (e) => setEvents(prev => [...prev, e]);
    return () => es.close();
  }, [url]);
  return events;
}

// Utils: camelCase
export function formatFriendlyError(error: string): string {
  // ...
}
```

**Hard rules:**
- Function components only (no class components)
- Explicit return type on top-level functions
- `setState` synchronously inside `useEffect` is a **lint error** (Course sacred rule) — derive or use ref
- No `@ts-nocheck` unless it's pre-existing on `Pets.tsx` (HFZ exception)

---

## 📝 Markdown / Docs

```markdown
# Title (H1)
Brief 1-2 sentence description.

## Section (H2)
### Subsection (H3)

**Bold** for emphasis, *italic* for terms, `inline code` for commands.

- Bulleted lists, parallel structure, capital first letter
1. Numbered for sequential steps

> Blockquotes for important notes

| Table | Headers |
|-------|---------|
| Data  | Values  |
```

For agent-facing docs, **always** add an explicit `## For AI Agents:` section.

---

## 🧩 Related Skills

- [[HS-076]] Pre-Commit Testing Checklist — what the lint gate runs
- [[HS-074]] FastAPI Agent API Standards — Python conventions in API context
- [[HS-085]] 5 Mandatory Agent Guardrails
