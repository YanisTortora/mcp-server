# tools.py
import ast, operator as op
from mcp import tool
from datetime import datetime
import uuid

# --- Sécurité : liste d'opérations autorisées ---
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
    """Évalue une expression mathématique en toute sécurité."""
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPS:
            return ALLOWED_OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPS:
            return ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("Expression invalide")

    tree = ast.parse(expr, mode="eval")
    return float(_eval(tree.body))

def calc_tool(expression: str):
    """
    Tool de calcul.
    Body attendu : { "expression": "2*(3+4)/7" }
    """
    result = safe_eval(expression)
    return {"result": result}

# 🔥 C'est ça que ton app.py lit
TOOLS = {
    "calc": calc_tool,
}
# Tu as déjà ça pour calc, on ajoute dessous :
REPORTS: list[dict] = []   # stockage simple pour le hackathon


@tool(
    name="create_report",
    description="Crée un ticket pour la conciergerie quand tu ne peux pas satisfaire une demande client.",
    input_schema={
        "type": "object",
        "properties": {
            "hotel_id": {
                "type": "string",
                "description": "Identifiant ou nom de l'hôtel concerné."
            },
            "customer_message": {
                "type": "string",
                "description": "Message original du client."
            },
            "reason": {
                "type": "string",
                "description": "Pourquoi l'IA ne peut pas répondre (ex: pas d'accès au planning)."
            },
            "conversation_id": {
                "type": "string",
                "description": "ID de conversation ou contexte si dispo.",
            }
        },
        "required": ["hotel_id", "customer_message", "reason"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "report_id": {"type": "string"},
            "status": {"type": "string"}
        },
        "required": ["report_id", "status"]
    }
)
def create_report(hotel_id: str, customer_message: str, reason: str, conversation_id: str | None = None):
    report_id = str(uuid.uuid4())
    report = {
        "id": report_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "hotel_id": hotel_id,
        "customer_message": customer_message,
        "reason": reason,
        "conversation_id": conversation_id,
        "status": "open"
    }
    REPORTS.append(report)
    return {"report_id": report_id, "status": "open"}

