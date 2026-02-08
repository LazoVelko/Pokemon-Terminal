#!/usr/bin/env node

const path = require("node:path");
const { spawn, spawnSync } = require("node:child_process");

const PACKAGE_ROOT = path.resolve(__dirname, "..");
const USER_ARGS = process.argv.slice(2);

function commandExists(command, args = []) {
  try {
    const result = spawnSync(command, [...args, "--version"], { encoding: "utf8" });
    if (result.status !== 0 || result.error) {
      return false;
    }

    const output = `${result.stdout || ""}\n${result.stderr || ""}`;
    const match = output.match(/Python\s+(\d+)\.(\d+)(?:\.\d+)?/i);
    if (!match) {
      return false;
    }

    const major = Number.parseInt(match[1], 10);
    const minor = Number.parseInt(match[2], 10);
    if (Number.isNaN(major) || Number.isNaN(minor)) {
      return false;
    }

    return major > 3 || (major === 3 && minor >= 10);
  } catch {
    return false;
  }
}

function resolvePython() {
  const candidates =
    process.platform === "win32"
      ? [
          { command: "py", args: ["-3"] },
          { command: "python", args: [] },
          { command: "python3", args: [] },
        ]
      : [
          { command: "python3", args: [] },
          { command: "python", args: [] },
        ];

  for (const candidate of candidates) {
    if (commandExists(candidate.command, candidate.args)) {
      return candidate;
    }
  }

  return null;
}

const python = resolvePython();
if (!python) {
  console.error("pokemon-terminal requires Python 3.10+ to run.");
  console.error("Install Python, then re-run `pokemon` or `ichooseyou`.");
  process.exit(1);
}

const child = spawn(
  python.command,
  [...python.args, "-m", "pokemonterminal.main", ...USER_ARGS],
  {
    stdio: "inherit",
    env: {
      ...process.env,
      PYTHONPATH: process.env.PYTHONPATH
        ? `${PACKAGE_ROOT}${path.delimiter}${process.env.PYTHONPATH}`
        : PACKAGE_ROOT,
    },
  },
);

child.on("close", (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
    return;
  }
  process.exit(code ?? 1);
});
