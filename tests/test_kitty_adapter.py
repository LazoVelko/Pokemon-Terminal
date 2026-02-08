import io
from pathlib import Path

from pokemonterminal.terminal.adapters import kitty
from pokemonterminal.terminal.adapters.kitty import KittyProvider


def test_kitty_compatible(monkeypatch):
    monkeypatch.setenv("KITTY_WINDOW_ID", "12")
    assert KittyProvider.is_compatible()
    monkeypatch.delenv("KITTY_WINDOW_ID")
    assert not KittyProvider.is_compatible()


def test_kitty_change_terminal_applies_background_and_colors(monkeypatch):
    calls = []

    def fake_run(args, check, capture_output):
        calls.append(args)

    monkeypatch.setattr(kitty, "run", fake_run)
    monkeypatch.setattr(kitty, "_infer_dark_threshold", lambda _: 0.9)
    monkeypatch.setattr(kitty, "_convert_to_png", lambda p: "/tmp/025.png")

    KittyProvider.change_terminal("/tmp/025.jpg")

    assert calls[0][:3] == ["kitty", "@", "set-background-image"]
    assert calls[0][3] == "/tmp/025.png"
    assert calls[1][:3] == ["kitty", "@", "set-colors"]
    assert any(arg.startswith("foreground=") for arg in calls[1][3:])


def test_kitty_text_mode_overrides(monkeypatch):
    monkeypatch.setattr(kitty, "_infer_dark_threshold", lambda _: 0.1)

    monkeypatch.setenv("POKEMON_TERMINAL_KITTY_TEXT_MODE", "dark")
    assert kitty._palette_for_path("/tmp/025.jpg") == kitty.LIGHT_BG_PALETTE

    monkeypatch.setenv("POKEMON_TERMINAL_KITTY_TEXT_MODE", "light")
    assert kitty._palette_for_path("/tmp/025.jpg") == kitty.DARK_BG_PALETTE

    monkeypatch.setenv("POKEMON_TERMINAL_KITTY_TEXT_MODE", "auto")
    assert kitty._palette_for_path("/tmp/025.jpg") == kitty.DARK_BG_PALETTE


def test_kitty_clear_resets_background_and_colors(monkeypatch):
    calls = []

    def fake_run(args, check, capture_output):
        calls.append(args)

    monkeypatch.setattr(kitty, "run", fake_run)
    KittyProvider.clear()

    assert calls[0] == ["kitty", "@", "set-background-image", "none"]
    assert calls[1] == ["kitty", "@", "set-colors", "--reset"]


def test_kitty_convert_png_passthrough(tmp_path):
    png = tmp_path / "x.png"
    png.write_bytes(b"\x89PNG\r\n\x1a\n")
    assert kitty._convert_to_png(str(png)) == str(png)


def test_kitty_convert_uses_cache_directory_tmp_file(tmp_path, monkeypatch):
    src = tmp_path / "x.jpg"
    src.write_bytes(b"jpg")
    target = tmp_path / "cache" / "out.png"
    target.parent.mkdir(parents=True, exist_ok=True)

    called = {}

    class DummyTmp:
        def __init__(self, name):
            self.name = str(name)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_named_temporary_file(*, dir, suffix, delete):
        called["dir"] = dir
        return DummyTmp(Path(dir) / "tmp-convert.png")

    def fake_run(args, check, capture_output):
        Path(args[-1]).write_bytes(b"\x89PNG\r\n\x1a\n")

    monkeypatch.setattr(kitty, "_cached_png_path", lambda _: target)
    monkeypatch.setattr(kitty.tempfile, "NamedTemporaryFile", fake_named_temporary_file)
    monkeypatch.setattr(kitty, "run", fake_run)

    out = kitty._convert_to_png(str(src))

    assert called["dir"] == str(target.parent)
    assert out == str(target)
    assert target.exists()


def test_load_dark_thresholds_skips_malformed_and_assigns_dense_ids(monkeypatch):
    data = "alpha 0.1\n\nbeta nope\ngamma 0.8\n"
    real_open = open

    def fake_open(path, *args, **kwargs):
        if str(path).endswith("pokemon.txt"):
            return io.StringIO(data)
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)
    kitty._load_dark_thresholds.cache_clear()
    by_id, by_name = kitty._load_dark_thresholds()
    kitty._load_dark_thresholds.cache_clear()

    assert by_id == {"001": 0.1, "002": 0.8}
    assert by_name == {"alpha": 0.1, "gamma": 0.8}
