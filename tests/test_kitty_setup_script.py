import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "kitty_setup.py"
SPEC = importlib.util.spec_from_file_location("kitty_setup", SCRIPT_PATH)
kitty_setup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kitty_setup)


def test_read_jsonc_valid(tmp_path):
    file_path = tmp_path / "settings.json"
    file_path.write_text('{"a": 1}', encoding="utf-8")
    assert kitty_setup._read_jsonc_file(file_path) == {"a": 1}


def test_read_jsonc_trailing_comma_object(tmp_path):
    file_path = tmp_path / "settings.json"
    file_path.write_text('{"a": 1,}', encoding="utf-8")
    assert kitty_setup._read_jsonc_file(file_path) == {"a": 1}


def test_read_jsonc_trailing_comma_array(tmp_path):
    file_path = tmp_path / "settings.json"
    file_path.write_text('{"a": [1, 2,],}', encoding="utf-8")
    assert kitty_setup._read_jsonc_file(file_path) == {"a": [1, 2]}


def test_read_jsonc_invalid_returns_none(tmp_path):
    file_path = tmp_path / "settings.json"
    file_path.write_text('{"a": 1,,}', encoding="utf-8")
    assert kitty_setup._read_jsonc_file(file_path) is None


def test_detect_vscode_target_darwin():
    path, platform_key = kitty_setup._detect_vscode_settings_target("darwin")
    assert platform_key == "osx"
    assert str(path).endswith("Library/Application Support/Code/User/settings.json")


def test_detect_vscode_target_linux():
    path, platform_key = kitty_setup._detect_vscode_settings_target("linux")
    assert platform_key == "linux"
    assert str(path).endswith(".config/Code/User/settings.json")


def test_detect_vscode_target_unsupported():
    path, platform_key = kitty_setup._detect_vscode_settings_target("win32")
    assert path is None
    assert platform_key is None


def test_replace_or_append_block_repairs_orphan_start(tmp_path):
    file_path = tmp_path / "sample.conf"
    file_path.write_text("alpha\n# START\norphan\n", encoding="utf-8")

    kitty_setup._replace_or_append_block(file_path, "# START", "# END", ["x=1"])
    updated = file_path.read_text(encoding="utf-8")
    assert "orphan" not in updated
    assert "# START\nx=1\n# END" in updated


def test_replace_or_append_block_repairs_orphan_end(tmp_path):
    file_path = tmp_path / "sample.conf"
    file_path.write_text("orphan\n# END\nomega\n", encoding="utf-8")

    kitty_setup._replace_or_append_block(file_path, "# START", "# END", ["x=1"])
    updated = file_path.read_text(encoding="utf-8")
    assert "orphan" not in updated
    assert "omega" in updated
    assert "# START\nx=1\n# END" in updated


def test_configure_vscode_preserves_comments_and_uses_block(tmp_path, monkeypatch):
    settings = tmp_path / "settings.json"
    settings.write_text(
        '{\n  // keep comment\n  "editor.fontSize": 20,\n}\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(kitty_setup, "VSCODE_SETTINGS", settings)
    monkeypatch.setattr(kitty_setup, "_VSCODE_PROFILE_PLATFORM", "osx")
    monkeypatch.setattr(
        kitty_setup,
        "_write_json_file",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("must not rewrite parsed JSON")),
    )

    assert kitty_setup._configure_vscode_default_kitty()
    updated = settings.read_text(encoding="utf-8")
    assert "// keep comment" in updated
    assert kitty_setup.VSCODE_BLOCK_START in updated
    assert '"terminal.integrated.defaultProfile.osx": "kitty"' in updated


def test_configure_vscode_unsupported_platform(monkeypatch):
    monkeypatch.setattr(kitty_setup, "VSCODE_SETTINGS", None)
    monkeypatch.setattr(kitty_setup, "_VSCODE_PROFILE_PLATFORM", None)
    assert not kitty_setup._configure_vscode_default_kitty()


def test_main_handles_eof_gracefully(tmp_path, monkeypatch, capsys):
    pokemon_bin = tmp_path / "pokemon"
    pokemon_bin.write_text("", encoding="utf-8")
    monkeypatch.setattr(kitty_setup, "POKEMON_BIN", pokemon_bin)

    def eof_input(_prompt):
        raise EOFError

    monkeypatch.setattr("builtins.input", eof_input)
    result = kitty_setup.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "No changes saved." in out


def test_main_handles_interrupt_in_loop(tmp_path, monkeypatch, capsys):
    pokemon_bin = tmp_path / "pokemon"
    pokemon_bin.write_text("", encoding="utf-8")
    monkeypatch.setattr(kitty_setup, "POKEMON_BIN", pokemon_bin)
    monkeypatch.setattr(kitty_setup, "_configure_vscode_default_kitty", lambda: True)
    monkeypatch.setattr(kitty_setup, "_configure_kitty_remote_control", lambda _password: None)

    answers = iter(["n", "n", "p"])

    def fake_input(_prompt):
        try:
            return next(answers)
        except StopIteration:
            raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", fake_input)
    result = kitty_setup.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "No changes saved." in out
