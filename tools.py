from mcp import tool
import ast, operator as op

# --- Sécurité : liste d'opérations autorisées ---
ALLOWED_OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
    ast.Pow: op.pow, ast.FloorDiv: op.floordiv, ast.Mod: op.mod, ast.USub: op.neg
}

def safe_eval(expr: str) -> float:
    """Évalue une expression mathématique en toute sécurité."""
    def _eval(node):
        if isinstance(node, ast.Num): return node.n
        if isinstance(node, ast.UnaryOp): return ALLOWED_OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp): return ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("Expression invalide")

    tree = ast.parse(expr, mode='eval')
    return float(_eval(tree.body))

# --- Déclaration du tool ---
@tool(
    name="calc",
    description="Effectue un calcul mathématique à partir d'une expression. Exemple : 2*(3+4)/7.",
    input_schema={
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "Expression mathématique à évaluer"}
        },
        "required": ["expression"]
    },
    output_schema={
        "type": "object",
        "properties": {"result": {"type": "number"}},
        "required": ["result"]
    }
)
def calc_tool(expression: str):
    try:
        result = safe_eval(expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
