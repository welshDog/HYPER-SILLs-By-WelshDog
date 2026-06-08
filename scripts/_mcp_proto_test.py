#!/usr/bin/env python3
"""Live MCP protocol smoke test — newline-delimited JSON (mcp SDK v1.26+ format)."""
import json, subprocess, sys, threading, queue, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path(__file__).parent.parent

proc = subprocess.Popen(
    [sys.executable, str(VAULT / "mcp_server.py")],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    cwd=str(VAULT),
)

q = queue.Queue()

def reader():
    for raw_line in proc.stdout:
        line = raw_line.decode("utf-8", "replace").strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            q.put(msg)
        except json.JSONDecodeError:
            pass

threading.Thread(target=reader, daemon=True).start()

def send(msg):
    proc.stdin.write((json.dumps(msg) + "\n").encode("utf-8"))
    proc.stdin.flush()

def recv(timeout=6):
    """Get next non-notification response."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            msg = q.get(timeout=0.5)
            # Skip server-side notifications; return only responses (have 'id' or 'result')
            if "id" in msg or "result" in msg:
                return msg
        except queue.Empty:
            continue
    return {}

# ── 1. Initialize ─────────────────────────────────────────────────────────────
send({"jsonrpc":"2.0","id":1,"method":"initialize","params":{
    "protocolVersion":"2024-11-05","capabilities":{},
    "clientInfo":{"name":"claude-code","version":"1.0"}
}})
init = recv()
si = init.get("result", {}).get("serverInfo", {})
caps = init.get("result", {}).get("capabilities", {})
print(f"[1] INIT   server={si.get('name')} proto={init.get('result',{}).get('protocolVersion')}")
print(f"     caps={list(caps.keys())}")

send({"jsonrpc":"2.0","method":"notifications/initialized","params":{}})
time.sleep(0.1)

# ── 2. List tools ─────────────────────────────────────────────────────────────
send({"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}})
tl = recv()
tools = tl.get("result", {}).get("tools", [])
names = [t["name"] for t in tools]
print(f"[2] TOOLS  ({len(names)}): {names}")

# ── 3. recommend_for_task ─────────────────────────────────────────────────────
send({"jsonrpc":"2.0","id":3,"method":"tools/call","params":{
    "name":"recommend_for_task",
    "arguments":{"task":"build a nightly self-improvement loop","limit":4}
}})
rec = recv()
data = json.loads(rec.get("result",{}).get("content",[{}])[0].get("text","{}"))
print(f"[3] RECOMMEND 'nightly self-improvement loop' ({data.get('count',0)} results):")
for s in data.get("recommended", []):
    print(f"     {s['id']:8}  {s['hero_name']:28}  score={s['relevance_score']}")

# ── 4. get_skill_graph on top result ──────────────────────────────────────────
top_id = data["recommended"][0]["id"] if data.get("recommended") else "HS-043"
send({"jsonrpc":"2.0","id":4,"method":"tools/call","params":{
    "name":"get_skill_graph",
    "arguments":{"skill_id": top_id}
}})
gr = recv()
g = json.loads(gr.get("result",{}).get("content",[{}])[0].get("text","{}"))
print(f"[4] GRAPH  {g.get('id')} {g.get('hero_name')} {g.get('emoji','')}")
print(f"     depends_on : {[(d['id'],d['hero_name'][:16]) for d in g.get('depends_on',[])]}")
print(f"     provides   : {g.get('provides',[])[:3]}")
print(f"     notes      : {g.get('graph_notes','')[:80]}")

# ── 5. search_skills ──────────────────────────────────────────────────────────
send({"jsonrpc":"2.0","id":5,"method":"tools/call","params":{
    "name":"search_skills",
    "arguments":{"query":"prometheus metrics","limit":3}
}})
sr = recv()
sd = json.loads(sr.get("result",{}).get("content",[{}])[0].get("text","{}"))
print(f"[5] SEARCH 'prometheus metrics' ({sd.get('count',0)} results):")
for s in sd.get("results", []):
    print(f"     {s['id']:8}  {s['hero_name']}")

# ── 6. load_skill ─────────────────────────────────────────────────────────────
send({"jsonrpc":"2.0","id":6,"method":"tools/call","params":{
    "name":"load_skill",
    "arguments":{"skill_id":"HS-093"}
}})
ls = recv()
ld = json.loads(ls.get("result",{}).get("content",[{}])[0].get("text","{}"))
gos = ld.get("gos", {})
print(f"[6] LOAD   {ld.get('id')} {ld.get('hero_name')}")
print(f"     content_length ={len(ld.get('content',''))} chars")
print(f"     gos.depends_on ={[d['id'] for d in gos.get('depends_on',[])]}")
print(f"     gos.provides   ={gos.get('provides',[])[:3]}")

proc.terminate()
proc.wait()
print("\nAll 6 MCP protocol calls OK.")
