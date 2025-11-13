from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from tools import TOOLS

app = FastAPI(title="MCP-like Python Tools Server")


@app.get("/health")
def health():
    return {"ok": True, "tools": sorted(list(TOOLS.keys()))}


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
        if hasattr(res, "__await__"):
            res = await res
        return JSONResponse({"ok": True, "result": res})
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Bad arguments: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
