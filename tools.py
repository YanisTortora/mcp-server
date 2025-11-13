# tools.py
import ast
import operator as op

# opérations autorisées
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
        if isinstance(node, ast.Num):        # nombre
            return node.n
        if isinstance(node, ast.UnaryOp):    # -x
            return ALLOWED_OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp):      # x + y, x * y, etc.
            return ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("Expression invalide")

    tree = ast.parse(expr, mode="eval")
    return float(_eval(tree.body))

def calc_tool(expression: str):
    """Fonction appelée par l’endpoint /tools/calc."""
    try:
        result = safe_eval(expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

# Dictionnaire des tools dispo pour app.py
TOOLS = {
    "calc": calc_tool,
}
