# HS-042 — 📋 SKILL REGISTRY AGENT — SkillRegistry Agent Pattern

## What it Does
Pattern for building an agent that maintains a live registry of all available skills, their versions, and capabilities. Enables dynamic skill discovery and routing in agent swarms.

## When To Use
- Building agent swarm orchestrators that need to discover skills at runtime
- Creating a skills marketplace or catalog
- Dynamic tool routing in multi-agent systems

## THE PATTERN
```python
# SkillRegistry Agent — FastAPI pattern
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

class Skill(BaseModel):
    id: str           # e.g. "HS-042"
    name: str         # e.g. "SKILL REGISTRY AGENT"
    version: str      # e.g. "v1.0"
    category: str     # agents / dev / broski / hypercode / web3
    description: str
    file_path: str
    tags: list[str]
    status: str       # rescued / catalogued / in-progress

# In-memory registry (swap for Redis/Postgres in prod)
registry: dict[str, Skill] = {}

@app.post('/skills')
async def register_skill(skill: Skill):
    registry[skill.id] = skill
    return {'registered': skill.id}

@app.get('/skills')
async def list_skills(category: Optional[str] = None):
    if category:
        return [s for s in registry.values() if s.category == category]
    return list(registry.values())

@app.get('/skills/{skill_id}')
async def get_skill(skill_id: str):
    return registry.get(skill_id)

@app.get('/skills/search/{query}')
async def search_skills(query: str):
    q = query.lower()
    return [s for s in registry.values()
            if q in s.name.lower() or q in s.description.lower()
            or any(q in tag for tag in s.tags)]

# Load from skills-registry.json
@app.on_event('startup')
async def load_registry():
    with open('skills-registry.json') as f:
        data = json.load(f)
    for skill in data.get('skills', []):
        registry[skill['id']] = Skill(**skill)
```

## Related Skills
- HS-080 THE TOOL BELT Universal Agent Tools API
- HS-089 THE GRAND ROSTER Hyper Agent Roster

---
*Source: HyperCode-V2.4 | Category: agents/*
