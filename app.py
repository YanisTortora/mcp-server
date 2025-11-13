# app.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from tools import TOOLS, REPORTS

app = FastAPI(title="MCP-like Python Tools Server")

@app.get("/")
def root():
    return {"ok": True}

@app.get("/health")
def health():
    return {"ok": True, "tools": sorted(list(TOOLS.keys()))}

@app.get("/reports")
def list_reports():
    # Endpoint pour le staff : voir tous les reports
    return {"count": len(REPORTS), "items": REPORTS}

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, request: Request):
    if tool_name not in TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    fn = TOOLS[tool_name]

    try:
        payload = await request.json()
    except Exception:
        payload = {}

    try:
        res = fn(**payload) if payload else fn()
        return JSONResponse({"ok": True, "result": res})
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Bad arguments: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports")
def get_reports():
    try:
        with open("reports.json", "r") as f:
            reports = json.load(f)
        return {"ok": True, "reports": reports}
    except FileNotFoundError:
        return {"ok": True, "reports": []}
