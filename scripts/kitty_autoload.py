#!/usr/bin/env python3
"""Apply persisted Pokemon-Terminal settings for Kitty sessions."""

import json
import os
import subprocess
from pathlib import Path


STATE_FILE = Path.home() / ".config" / "pokemon-terminal" / "kitty-profile.json"


def _load_state():
    if not STATE_FILE.exists():
        return None
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None


def _build_command(state):
    pokemon_bin = state.get("pokemon_binary", "pokemon")
    selector = str(state.get("pokemon_selector", "")).strip()
    if not selector:
        return [pokemon_bin]
    if selector.isdigit():
        return [pokemon_bin, selector]
    return [pokemon_bin, "-n", selector]


def main():
    if "KITTY_WINDOW_ID" not in os.environ:
        return 0

    state = _load_state()
    if not state:
        return 0

    env = os.environ.copy()
    text_mode = str(state.get("text_mode", "auto")).lower()
    env["POKEMON_TERMINAL_KITTY_TEXT_MODE"] = text_mode

    rc_password = state.get("kitty_rc_password")
    if rc_password:
        env["KITTY_RC_PASSWORD"] = rc_password

    cmd = _build_command(state)
    try:
        subprocess.run(cmd, check=False, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
