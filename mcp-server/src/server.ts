import path from "node:path";
import { fileURLToPath } from "node:url";
import { randomUUID } from "node:crypto";
import fs from "node:fs/promises";
import express, { Request, Response } from "express";
import { z } from "zod";
import { glob } from "glob";
import matter from "gray-matter";

import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";

/** Basic config: assume server lives at repo/mcp-server and repo root is up one level */
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(path.join(__dirname, "..", ".."));

function md(pathRel: string) {
  return path.join(REPO_ROOT, pathRel);
}

async function readTextIfExists(p: string) {
  try { return await fs.readFile(p, "utf8"); } catch { return undefined; }
}

const server = new McpServer({ name: "semantic-architecture-mcp", version: "0.1.0" });

/** RESOURCES: Expose your core docs as named resources */
server.registerResource(
  "project-vision",
  new ResourceTemplate("semantic-architecture://vision", { list: undefined }),
  { title: "Project Vision", description: "VISION.md from the repo" },
  async (uri) => ({
    contents: [{ uri: uri.href, text: (await readTextIfExists(md("VISION.md"))) ?? "# Missing VISION.md" }]
  })
);

server.registerResource(
  "collaboration-model",
  new ResourceTemplate("semantic-architecture://collaboration-model", { list: undefined }),
  { title: "Semantic Collaboration Model", description: "Semantic Collaboration Model.md from the repo" },
  async (uri) => ({
    contents: [{
      uri: uri.href,
      text: (await readTextIfExists(md("Semantic Collaboration Model.md"))) ?? "# Missing Collaboration Model"
    }]
  })
);

server.registerResource(
  "project-model",
  new ResourceTemplate("semantic-architecture://project-model", { list: undefined }),
  { title: "Semantic Project Model", description: "Semantic Project Model.md from the repo" },
  async (uri) => ({
    contents: [{
      uri: uri.href,
      text: (await readTextIfExists(md("Semantic Project Model.md"))) ?? "# Missing Project Model"
    }]
  })
);

/** TOOL: Build a lightweight semantic map from folder structure */
server.registerTool(
  "semantic.map",
  {
    title: "Build Semantic Map",
    description: "Infer Project → Cluster → Module hierarchy from repo folders",
    inputSchema: {
      root: z.string().optional().describe("Relative path to scan, default '.'")
    },
    outputSchema: {
      project: z.string(),
      clusters: z.array(z.object({
        name: z.string(),
        modules: z.array(z.string())
      }))
    }
  },
  async ({ root }) => {
    const base = path.resolve(REPO_ROOT, root ?? ".");
    // Heuristic: /clusters/<cluster>/<module> or /modules/<module>
    const clusters: Record<string, Set<string>> = {};

    const clusterPaths = await glob(["clusters/*/*/"], { cwd: base, dot: true, withFileTypes: false });
    for (const cp of clusterPaths) {
      const [, cluster, module] = cp.split(path.sep);
      clusters[cluster] ??= new Set();
      clusters[cluster].add(module);
    }

    // also support flat modules/ path
    const flatModules = await glob(["modules/*/"], { cwd: base });
    if (flatModules.length) {
      clusters["default"] ??= new Set();
      for (const m of flatModules) clusters["default"].add(m.split(path.sep)[1]);
    }

    const result = {
      project: path.basename(REPO_ROOT),
      clusters: Object.entries(clusters).map(([name, mods]) => ({ name, modules: [...mods].sort() }))
    };

    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

/** TOOL: Validate each semantic module has about.md + semantic-instructions.md */
server.registerTool(
  "semantic.validate",
  {
    title: "Validate Semantic Modules",
    description: "Ensure each module folder contains about.md and semantic-instructions.md",
    inputSchema: {
      root: z.string().optional()
    },
    outputSchema: {
      ok: z.boolean(),
      modules: z.array(z.object({
        path: z.string(),
        hasAbout: z.boolean(),
        hasInstructions: z.boolean()
      })),
      missing: z.array(z.object({ path: z.string(), missing: z.array(z.string()) }))
    }
  },
  async ({ root }) => {
    const base = path.resolve(REPO_ROOT, root ?? ".");
    const moduleDirs = [
      ...(await glob(["clusters/*/*/"], { cwd: base })),
      ...(await glob(["modules/*/"], { cwd: base }))
    ];

    const modules = await Promise.all(moduleDirs.map(async d => {
      const p = path.join(base, d);
      const hasAbout = !!(await readTextIfExists(path.join(p, "about.md")));
      const hasInstructions = !!(await readTextIfExists(path.join(p, "semantic-instructions.md")));
      return { path: d, hasAbout, hasInstructions };
    }));

    const missing = modules
      .filter(m => !m.hasAbout || !m.hasInstructions)
      .map(m => ({
        path: m.path,
        missing: [
          ...(!m.hasAbout ? ["about.md"] : []),
          ...(!m.hasInstructions ? ["semantic-instructions.md"] : [])
        ]
      }));

    const ok = missing.length === 0;

    return {
      content: [{ type: "text", text: JSON.stringify({ ok, missing }, null, 2) }],
      structuredContent: { ok, modules, missing }
    };
  }
);

/** TOOL: Scaffold a new semantic module */
server.registerTool(
  "semantic.initModule",
  {
    title: "Create Semantic Module",
    description: "Scaffold a module with about.md and semantic-instructions.md",
    inputSchema: {
      name: z.string(),
      cluster: z.string().optional().describe("Optional cluster name")
    },
    outputSchema: { path: z.string() }
  },
  async ({ name, cluster }) => {
    const base = cluster
      ? path.join(REPO_ROOT, "clusters", cluster, name)
      : path.join(REPO_ROOT, "modules", name);

    await fs.mkdir(base, { recursive: true });

    const about = `# ${name}\n\nPurpose, inputs/outputs, invariants.\n`;
    const instructions = `# Semantic Instructions for ${name}\n\n- Boundaries\n- Allowed changes\n- Tests to run\n`;

    await fs.writeFile(path.join(base, "about.md"), about, "utf8");
    await fs.writeFile(path.join(base, "semantic-instructions.md"), instructions, "utf8");

    return {
      content: [{ type: "text", text: `Created module at ${path.relative(REPO_ROOT, base)}` }],
      structuredContent: { path: path.relative(REPO_ROOT, base) }
    };
  }
);

/** HTTP transport for VS Code / Copilot */
const app = express();
app.use(express.json());

app.post("/mcp", async (req: Request, res: Response) => {
  const transport = new StreamableHTTPServerTransport({ 
    enableJsonResponse: true,
    sessionIdGenerator: () => randomUUID()
  });
  res.on("close", () => transport.close());
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

const port = parseInt(process.env.PORT || "3000", 10);
app.listen(port, () => {
  console.log(`Semantic Architecture MCP running on http://localhost:${port}/mcp`);
}).on("error", (err: Error) => {
  console.error(err);
  process.exit(1);
});
