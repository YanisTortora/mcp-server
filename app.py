# app.py
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from tools import TOOLS
import os

app = FastAPI(title="MCP-like Python Tools Server")

# (optionnel) petite clé API pour les calls depuis Azure
API_KEY = os.getenv("API_KEY", "dev-key")

def check_key(x_api_key: str | None):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/")
def root():
    return {"ok": True}

@app.get("/health")
def health():
    return {"ok": True, "tools": sorted(list(TOOLS.keys()))}

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, request: Request, x_api_key: str | None = Header(None)):
    check_key(x_api_key)

    if tool_name not in TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

    fn = TOOLS[tool_name]
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    try:
        res = fn(**payload) if payload else fn()
        # support async tools
        if hasattr(res, "__await__"):
            res = await res
        return JSONResponse({"ok": True, "result": res})
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Bad arguments: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
