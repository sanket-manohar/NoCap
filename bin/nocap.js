#!/usr/bin/env node
/**
 * NoCap CLI for Node users — no global install needed:
 *
 *   npx github:sanket-manohar/nocap init          # install into current project
 *   npx github:sanket-manohar/nocap init --ci --tools cursor,claude
 *   npx github:sanket-manohar/nocap scan [path]   # run the scanner (needs Python 3.8+)
 *   npx github:sanket-manohar/nocap prompt        # print the master prompt to paste anywhere
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const SRC = path.resolve(__dirname, "..");
const START = "<!-- nocap:start -->";
const END = "<!-- nocap:end -->";
const TOOL_OF = [
  [/^AGENTS\.md$/, "generic"], [/^(CLAUDE\.md|\.claude\/)/, "claude"], [/^\.cursor\//, "cursor"],
  [/^\.github\/(copilot-instructions\.md|prompts\/)/, "copilot"], [/^\.windsurf\//, "windsurf"],
  [/^\.clinerules\//, "cline"], [/^\.roo\//, "roo"], [/^\.continue\//, "continue"], [/^GEMINI\.md$/, "gemini"],
  [/^\.junie\//, "junie"], [/^\.aider\.conf\.yml$/, "aider"],
];
const toolOf = (d) => (TOOL_OF.find(([re]) => re.test(d)) || [null, "other"])[1];
const paint = (c, s) => (process.stdout.isTTY ? `\x1b[${c}m${s}\x1b[0m` : s);

function copyDir(from, to) {
  fs.mkdirSync(to, { recursive: true });
  for (const e of fs.readdirSync(from, { withFileTypes: true })) {
    const a = path.join(from, e.name), b = path.join(to, e.name);
    e.isDirectory() ? copyDir(a, b) : fs.copyFileSync(a, b);
  }
}
function stripBlock(text) {
  const out = []; let skip = false;
  for (const l of text.split(/\r?\n/)) {
    if (l === START) { skip = true; continue; }
    if (l === END) { skip = false; continue; }
    if (!skip) out.push(l);
  }
  return out.join("\n").replace(/\n+$/, "");
}

function init(args) {
  let target = ".", tools = null;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--tools") tools = (args[++i] || "").split(",");
    else if (!args[i].startsWith("--")) target = args[i];
  }
  target = path.resolve(target);
  console.log(`\n  ${paint("1;35", "NoCap")}  installing into ${target}\n`);
  const vp = path.join(target, ".nocap");
  fs.rmSync(vp, { recursive: true, force: true });
  for (const d of ["prompts", "templates", "checklists"]) copyDir(path.join(SRC, d), path.join(vp, d));
  for (const f of ["AGENTS.md", "MASTER_PROMPT.md", "TERMS.md", "LICENSE"]) fs.copyFileSync(path.join(SRC, f), path.join(vp, f));
  fs.mkdirSync(path.join(vp, "scanner"), { recursive: true });
  fs.copyFileSync(path.join(SRC, "scanner", "nocap.py"), path.join(vp, "scanner", "nocap.py"));
  fs.writeFileSync(path.join(vp, ".nocap-toolkit"), "");
  fs.writeFileSync(path.join(vp, "vp"), '#!/usr/bin/env sh\nDIR="$(cd "$(dirname "$0")" && pwd)"\nPY="$(command -v python3 || command -v python)"\nexec "$PY" "$DIR/scanner/nocap.py" "${@:-.}"\n', { mode: 0o755 });
  fs.writeFileSync(path.join(vp, "vp.cmd"), '@echo off\r\nwhere py >nul 2>nul && (py -3 "%~dp0scanner\\nocap.py" %*) || (python "%~dp0scanner\\nocap.py" %*)\r\n');
  console.log(`  ${paint("35", "▸")} Toolkit      → .nocap/`);

  const lines = fs.readFileSync(path.join(SRC, "adapters", "MANIFEST"), "utf8").split(/\r?\n/).filter((l) => l && !l.startsWith("#"));
  for (const line of lines) {
    const [mode, src, dest] = line.split(" ");
    const t = toolOf(dest);
    if (tools && !tools.includes(t)) continue;
    const f = path.join(target, dest);
    fs.mkdirSync(path.dirname(f), { recursive: true });
    const body = fs.readFileSync(path.join(SRC, src), "utf8");
    if (mode === "copy") fs.writeFileSync(f, body);
    else if (mode === "copy-if-missing") { if (!fs.existsSync(f)) fs.writeFileSync(f, body); }
    else if (mode === "merge") {
      const prev = fs.existsSync(f) ? stripBlock(fs.readFileSync(f, "utf8")) : "";
      fs.writeFileSync(f, (prev ? prev + "\n\n" : "") + `${START}\n${body.replace(/\n$/, "")}\n${END}\n`);
    }
    console.log(`  ${paint("32", "✓")} ${t.padEnd(12)} → ${dest}`);
  }
  if (args.includes("--ci")) {
    const wf = path.join(target, ".github", "workflows");
    fs.mkdirSync(wf, { recursive: true });
    fs.copyFileSync(path.join(SRC, "adapters", "ci", "nocap.yml"), path.join(wf, "nocap.yml"));
    console.log(`  ${paint("35", "▸")} CI workflow  → .github/workflows/nocap.yml`);
  }
  const gi = path.join(target, ".gitignore");
  const giText = fs.existsSync(gi) ? fs.readFileSync(gi, "utf8") : "";
  if (!giText.includes("nocap-results.json")) fs.appendFileSync(gi, "\n# NoCap\n.nocap-results.json\n");
  console.log(`\n  ${paint("1;32", "✔ NoCap installed!")}\n\n  Open your AI assistant and type:  ${paint("1;36", "nocap docs")}  ·  ${paint("1;36", "nocap audit")}  ·  ${paint("1;36", "nocap ship")}\n  Run the scanner:                  ${paint("1;36", "npx github:sanket-manohar/nocap scan")}\n\n  ⚠ Development aid only — final checks are your responsibility. See .nocap/TERMS.md\n`);
}

function scan(args) {
  const script = path.join(SRC, "scanner", "nocap.py");
  for (const py of process.platform === "win32" ? [["py", "-3"], ["python"]] : [["python3"], ["python"]]) {
    const r = spawnSync(py[0], [...py.slice(1), script, ...(args.length ? args : ["."])], { stdio: "inherit" });
    if (!r.error) process.exit(r.status ?? 0);
  }
  console.error("NoCap scanner needs Python 3.8+ → https://www.python.org/downloads/\n" +
    "No Python? Ask your AI assistant: 'nocap score' — it computes the same score manually.");
  process.exit(2);
}

const [cmd = "help", ...rest] = process.argv.slice(2);
if (cmd === "init" || cmd === "install") init(rest);
else if (cmd === "scan") scan(rest);
else if (cmd === "prompt") process.stdout.write(fs.readFileSync(path.join(SRC, "MASTER_PROMPT.md"), "utf8"));
else console.log(`
  NoCap — documentation + security for AI-built software

  Usage:
    npx github:sanket-manohar/nocap init [dir] [--tools cursor,claude,...] [--ci]
    npx github:sanket-manohar/nocap scan [dir] [--fail-on high] [--badge badge.svg]
    npx github:sanket-manohar/nocap prompt     # print the copy-paste master prompt
`);
