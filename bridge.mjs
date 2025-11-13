import express from "express";
import { spawn } from "node:child_process";

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/transport/stdio.js";

const app = express();
app.use(express.json());

// Lance le serveur MCP Python (STDIO)
const mcpProc = spawn("python3", ["mcp_server.py"], { stdio: ["pipe","pipe","pipe"] });
mcpProc.stderr.on("data", d => process.stderr.write(d));

const transport = new StdioClientTransport(mcpProc.stdin, mcpProc.stdout);
const client = new Client({ name: "concierge-bridge", version: "1.0.0" });
await client.connect(transport);

// Health: liste les tools
app.get("/health", async (_, res) => {
  try {
    const list = await client.listTools();
    res.json({ ok: true, tools: (list.tools || []).map(t => t.name) });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

const PORT = process.env.PORT || 8787;
app.listen(PORT, () => console.log(`✅ MCP Bridge running on :${PORT}`));
