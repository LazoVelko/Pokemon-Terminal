import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "kitty_autoload.py"
SPEC = importlib.util.spec_from_file_location("kitty_autoload", SCRIPT_PATH)
kitty_autoload = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kitty_autoload)


def test_build_command_name():
    state = {"pokemon_binary": "/tmp/pokemon", "pokemon_selector": "pikachu"}
    assert kitty_autoload._build_command(state) == ["/tmp/pokemon", "-n", "pikachu"]


def test_build_command_id():
    state = {"pokemon_binary": "/tmp/pokemon", "pokemon_selector": "25"}
    assert kitty_autoload._build_command(state) == ["/tmp/pokemon", "25"]


def test_main_no_kitty(monkeypatch):
    monkeypatch.delenv("KITTY_WINDOW_ID", raising=False)
    assert kitty_autoload.main() == 0
