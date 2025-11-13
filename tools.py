# tools.py
import ast, operator as op

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
