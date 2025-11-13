from fastmcp import FastMCP

app = FastMCP(name="concierge-mcp", version="1.0.0")

# ➜ Tu ajouteras des outils ici plus tard avec @app.tool()

if __name__ == "__main__":
    app.run()
