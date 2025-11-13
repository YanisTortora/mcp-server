import express from "express";
import { tools } from "./tools.mjs";

const app = express();
app.use(express.json());

// Health: liste des tools disponibles
app.get("/health", (_, res) => {
  res.json({ ok: true, tools: Object.keys(tools) });
});

// Endpoint générique pour appeler un tool
app.post("/tools/:toolName", async (req, res) => {
  const { toolName } = req.params;
  const fn = tools[toolName];
  if (!fn) return res.status(404).json({ ok: false, error: `Tool '${toolName}' not found` });
  try {
    const out = await fn(req.body || {});
    res.json({ ok: true, result: out });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

const PORT = process.env.PORT || 8787;
app.listen(PORT, () => console.log(`✅ MCP-like HTTP server running on :${PORT}`));
