# tools.py
import ast
import operator as op
from datetime import datetime

# ====== CALCUL ======

ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}

def safe_eval(expr: str) -> float:
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.UnaryOp):
            return ALLOWED_OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp):
            return ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("Expression invalide")

    tree = ast.parse(expr, mode="eval")
    return float(_eval(tree.body))

def calc_tool(expression: str):
    try:
        result = safe_eval(expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


# ====== REPORTING ======

# stockage ultra simple en mémoire (OK pour un hackathon)
REPORTS: list[dict] = []

def report_issue(
    message: str,
    guest_id: str | None = None,
    category: str | None = None,
    agent_notes: str | None = None,
):
    """
    Enregistre une demande que l’IA ne sait pas gérer,
    pour que le staff puisse la traiter plus tard.
    """
    report = {
        "id": len(REPORTS) + 1,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "guest_id": guest_id,
        "category": category,
        "message": message,
        "agent_notes": agent_notes,
        "status": "open",
    }
    REPORTS.append(report)
    return {"ok": True, "report": report}


# ====== REGISTRE DES TOOLS ======

TOOLS = {
    "calc": calc_tool,
    "report_issue": report_issue,
}
