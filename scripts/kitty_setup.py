#!/usr/bin/env python3
"""Interactive setup for Kitty + VS Code + Pokemon-Terminal persistence."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
POKEMON_BIN = REPO_ROOT / ".venv" / "bin" / "pokemon"
PYTHON_BIN = REPO_ROOT / ".venv" / "bin" / "python"
AUTOLOAD_SCRIPT = REPO_ROOT / "scripts" / "kitty_autoload.py"

CONFIG_DIR = Path.home() / ".config" / "pokemon-terminal"
STATE_FILE = CONFIG_DIR / "kitty-profile.json"
KITTY_CONF = Path.home() / ".config" / "kitty" / "kitty.conf"
ZSHRC = Path.home() / ".zshrc"

KITTY_BLOCK_START = "# >>> pokemon-terminal kitty >>>"
KITTY_BLOCK_END = "# <<< pokemon-terminal kitty <<<"
ZSH_BLOCK_START = "# >>> pokemon-terminal kitty autoload >>>"
ZSH_BLOCK_END = "# <<< pokemon-terminal kitty autoload <<<"
VSCODE_BLOCK_START = "// >>> pokemon-terminal vscode >>>"
VSCODE_BLOCK_END = "// <<< pokemon-terminal vscode <<<"


def _detect_vscode_settings_target(platform_name=None):
    platform_name = platform_name or sys.platform
    if platform_name == "darwin":
        return (
            Path.home() / "Library" / "Application Support" / "Code" / "User" / "settings.json",
            "osx",
        )
    if platform_name.startswith("linux"):
        return (
            Path.home() / ".config" / "Code" / "User" / "settings.json",
            "linux",
        )
    return None, None


VSCODE_SETTINGS, _VSCODE_PROFILE_PLATFORM = _detect_vscode_settings_target()


def _read_json_file(path: Path):
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}


def _strip_json_comments(text: str) -> str:
    def replacer(match: re.Match):
        token = match.group(0)
        if token.startswith("/"):
            return " "
        return token

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    return re.sub(pattern, replacer, text)


def _strip_trailing_commas(text: str) -> str:
    output = []
    in_string = False
    string_quote = ""
    escape = False

    for i, char in enumerate(text):
        if in_string:
            output.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == string_quote:
                in_string = False
                string_quote = ""
            continue

        if char in {'"', "'"}:
            in_string = True
            string_quote = char
            output.append(char)
            continue

        if char == ",":
            j = i + 1
            while j < len(text) and text[j].isspace():
                j += 1
            if j < len(text) and text[j] in "]}":
                continue

        output.append(char)

    return "".join(output)


def _read_jsonc_file(path: Path):
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            raw = handle.read().strip()
        if not raw:
            return {}
        normalized = _strip_trailing_commas(_strip_json_comments(raw))
        return json.loads(normalized)
    except OSError:
        return None
    except json.JSONDecodeError:
        return None


def _write_json_file(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def _replace_or_append_block(path: Path, start: str, end: str, block_lines):
    content = ""
    if path.exists():
        with open(path, "r", encoding="utf-8") as handle:
            content = handle.read()
    block = "\n".join([start, *block_lines, end]) + "\n"
    has_start = start in content
    has_end = end in content
    replaced = False

    if has_start and has_end:
        start_idx = content.find(start)
        end_idx = content.find(end, start_idx + len(start))
        if end_idx != -1:
            cut_end = end_idx + len(end)
            if cut_end < len(content) and content[cut_end] == "\n":
                cut_end += 1
            content = content[:start_idx] + block + content[cut_end:]
            replaced = True
        else:
            has_end = False

    if not replaced and has_start and not has_end:
        print(f"Warning: found orphan start marker in {path}; repairing.")
        content = content[:content.find(start)]

    if not replaced and has_end and not has_start:
        print(f"Warning: found orphan end marker in {path}; repairing.")
        cut_start = content.find(end) + len(end)
        if cut_start < len(content) and content[cut_start] == "\n":
            cut_start += 1
        content = content[cut_start:]

    if not replaced:
        if content and not content.endswith("\n"):
            content += "\n"
        content += ("\n" if content else "") + block
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def _strip_orphan_or_existing_marker_block(content: str, start: str, end: str, path: Path):
    has_start = start in content
    has_end = end in content

    if has_start and has_end:
        start_idx = content.find(start)
        end_idx = content.find(end, start_idx + len(start))
        if end_idx != -1:
            cut_end = end_idx + len(end)
            if cut_end < len(content) and content[cut_end] == "\n":
                cut_end += 1
            return content[:start_idx] + content[cut_end:]
        has_end = False

    if has_start and not has_end:
        print(f"Warning: found orphan start marker in {path}; repairing.")
        return content[:content.find(start)]

    if has_end and not has_start:
        print(f"Warning: found orphan end marker in {path}; repairing.")
        cut_start = content.find(end) + len(end)
        if cut_start < len(content) and content[cut_start] == "\n":
            cut_start += 1
        return content[cut_start:]

    return content


def _insert_vscode_settings_block(content: str, profile_platform: str, path: Path):
    if not content.strip():
        content = "{}\n"

    content = _strip_orphan_or_existing_marker_block(
        content, VSCODE_BLOCK_START, VSCODE_BLOCK_END, path
    )

    object_start = content.find("{")
    object_end = content.rfind("}")
    if object_start == -1 or object_end == -1 or object_start > object_end:
        print(f"Skipping VS Code settings update (unexpected JSON structure in {path}).")
        return None

    block = "\n".join(
        [
            f"  {VSCODE_BLOCK_START}",
            f'  "terminal.integrated.profiles.{profile_platform}": {{',
            '    "kitty": {',
            '      "path": "kitty"',
            "    }",
            "  },",
            f'  "terminal.integrated.defaultProfile.{profile_platform}": "kitty"',
            f"  {VSCODE_BLOCK_END}",
        ]
    )

    head = content[:object_end].rstrip()
    tail = content[object_end:]
    body = content[object_start + 1:object_end].strip()
    if body and not head.endswith(","):
        head += ","
    updated = head + "\n" + block + "\n" + tail.lstrip()
    if not updated.endswith("\n"):
        updated += "\n"
    return updated


def _configure_vscode_default_kitty():
    if VSCODE_SETTINGS is None or _VSCODE_PROFILE_PLATFORM is None:
        print("Skipping VS Code settings update (unsupported platform).")
        return False

    raw = "{}\n"
    if VSCODE_SETTINGS.exists():
        try:
            with open(VSCODE_SETTINGS, "r", encoding="utf-8") as handle:
                raw = handle.read()
        except OSError:
            print(f"Skipping VS Code settings update (unable to read {VSCODE_SETTINGS}).")
            return False

    updated = _insert_vscode_settings_block(raw, _VSCODE_PROFILE_PLATFORM, VSCODE_SETTINGS)
    if updated is None:
        return False

    VSCODE_SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    with open(VSCODE_SETTINGS, "w", encoding="utf-8") as handle:
        handle.write(updated)
    return True


def _configure_kitty_remote_control(password: str):
    remote_line = f'remote_control_password "{password}" set-background-image set-colors'
    _replace_or_append_block(
        KITTY_CONF,
        KITTY_BLOCK_START,
        KITTY_BLOCK_END,
        [
            "allow_remote_control password",
            remote_line,
        ],
    )


def _install_zsh_autoload_hook():
    python_bin = str(PYTHON_BIN).replace('"', '\\"')
    autoload_script = str(AUTOLOAD_SCRIPT).replace('"', '\\"')
    block_lines = [
        "if [[ -n \"$KITTY_WINDOW_ID\" && -o interactive ]]; then",
        f"  if [[ -x \"{python_bin}\" && -f \"{autoload_script}\" ]]; then",
        f"    \"{python_bin}\" \"{autoload_script}\"",
        "  fi",
        "fi",
    ]
    _replace_or_append_block(ZSHRC, ZSH_BLOCK_START, ZSH_BLOCK_END, block_lines)


def _run_preview(selector: str, text_mode: str, password: str):
    if "KITTY_WINDOW_ID" not in os.environ:
        print("Not in a Kitty terminal, skipping live preview.")
        return

    env = os.environ.copy()
    env["POKEMON_TERMINAL_KITTY_TEXT_MODE"] = text_mode
    if password:
        env["KITTY_RC_PASSWORD"] = password

    cmd = [str(POKEMON_BIN)]
    selector = selector.strip()
    if selector:
        if selector.isdigit():
            cmd.append(selector)
        else:
            cmd.extend(["-n", selector.lower()])
    cmd.append("-v")
    subprocess.run(cmd, check=False, env=env)


def _save_state(selector: str, text_mode: str, password: str):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "pokemon_selector": selector.strip(),
        "text_mode": text_mode,
        "kitty_rc_password": password,
        "pokemon_binary": str(POKEMON_BIN),
    }
    _write_json_file(STATE_FILE, payload)
    STATE_FILE.chmod(0o600)


def _prompt(prompt: str, default: str):
    value = input(f"{prompt} [{default}]: ").strip()
    return value if value else default


def _prompt_yes_no(prompt: str, default_yes=True):
    suffix = "Y/n" if default_yes else "y/N"
    value = input(f"{prompt} ({suffix}): ").strip().lower()
    if not value:
        return default_yes
    return value in {"y", "yes"}


def main():
    print("Pokemon-Terminal Kitty Setup Wizard")
    print("-----------------------------------")
    if not POKEMON_BIN.exists():
        print(f"Missing {POKEMON_BIN}. Run `make setup` first.")
        return 1

    existing = _read_json_file(STATE_FILE)
    selector = str(existing.get("pokemon_selector", "pikachu"))
    text_mode = str(existing.get("text_mode", "auto")).lower()
    if text_mode not in {"auto", "light", "dark"}:
        text_mode = "auto"
    password = str(existing.get("kitty_rc_password", "missingno"))

    try:
        if _prompt_yes_no("Set Kitty as default terminal profile in VS Code?", True):
            if _configure_vscode_default_kitty():
                print(f"Updated {VSCODE_SETTINGS}")

        if _prompt_yes_no("Configure Kitty remote control block in kitty.conf?", True):
            password = _prompt("Kitty remote-control password", password)
            _configure_kitty_remote_control(password)
            print(f"Updated {KITTY_CONF}")

        while True:
            print("")
            print(f"Current selector: {selector or '(random each start)'}")
            print(f"Current text mode: {text_mode}")
            print("Actions: [p] preview pokemon  [r] random preview  [m] text mode  [s] save+enable  [q] quit")
            choice = input("Choose action: ").strip().lower()

            if choice == "p":
                selector = input("Pokemon name or id: ").strip().lower()
                if selector:
                    _run_preview(selector, text_mode, password)
            elif choice == "r":
                selector = ""
                _run_preview(selector, text_mode, password)
            elif choice == "m":
                mode = _prompt("Text mode (auto/light/dark)", text_mode).lower()
                if mode in {"auto", "light", "dark"}:
                    text_mode = mode
                    _run_preview(selector, text_mode, password)
                else:
                    print("Invalid mode.")
            elif choice == "s":
                _save_state(selector, text_mode, password)
                _install_zsh_autoload_hook()
                print(f"Saved profile: {STATE_FILE}")
                print(f"Installed autoload hook in {ZSHRC}")
                print("Open a new Kitty tab/window to see the saved theme applied automatically.")
                return 0
            elif choice == "q":
                print("No changes saved.")
                return 0
            else:
                print("Invalid option.")
    except (EOFError, KeyboardInterrupt):
        print("\nNo changes saved.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
