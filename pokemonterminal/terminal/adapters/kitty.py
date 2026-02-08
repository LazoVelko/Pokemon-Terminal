import os
import sys
import tempfile
from hashlib import sha1
from functools import lru_cache
from pathlib import Path
from subprocess import CalledProcessError, run

from . import TerminalProvider as _TProv

LIGHT_BG_PALETTE = {
    "foreground": "#111111",
    "cursor": "#111111",
    "selection_foreground": "#111111",
    "selection_background": "#d6d6d6",
    "color0": "#111111",
    "color1": "#8f1d21",
    "color2": "#1f7a32",
    "color3": "#6b5800",
    "color4": "#004f95",
    "color5": "#6a2e8a",
    "color6": "#006c79",
    "color7": "#8f8f8f",
    "color8": "#4d4d4d",
    "color9": "#b33a3f",
    "color10": "#2f9951",
    "color11": "#8c7300",
    "color12": "#2a73ba",
    "color13": "#8d3ab5",
    "color14": "#008b9c",
    "color15": "#111111",
}

DARK_BG_PALETTE = {
    "foreground": "#f0f0f0",
    "cursor": "#f0f0f0",
    "selection_foreground": "#111111",
    "selection_background": "#f0f0f0",
    "color0": "#1a1a1a",
    "color1": "#ff6b6b",
    "color2": "#8ce99a",
    "color3": "#ffd43b",
    "color4": "#74c0fc",
    "color5": "#d0bfff",
    "color6": "#66d9e8",
    "color7": "#dee2e6",
    "color8": "#6c757d",
    "color9": "#ff8787",
    "color10": "#b2f2bb",
    "color11": "#ffe066",
    "color12": "#a5d8ff",
    "color13": "#e5dbff",
    "color14": "#99e9f2",
    "color15": "#ffffff",
}


def print_kitty_error(err: CalledProcessError, action: str):
    print(f"Failed to {action} in kitty. Did you configure"
          " kitty remote control correctly? (See Readme).")
    if msg := err.stderr:
        print(f"Output from kitty: \"{msg.decode().strip()}\".")


@lru_cache(maxsize=1)
def _load_dark_thresholds():
    data_path = Path(__file__).resolve().parents[2] / "Data" / "pokemon.txt"
    by_id = {}
    by_name = {}
    id_counter = 1
    with open(data_path, "r", encoding="utf-8") as data_file:
        for line in data_file:
            pokemon_data = line.split()
            if len(pokemon_data) < 2:
                continue
            name = pokemon_data[0].lower()
            try:
                threshold = float(pokemon_data[1])
            except (ValueError, TypeError):
                continue
            by_name[name] = threshold
            by_id[f"{id_counter:03d}"] = threshold
            id_counter += 1
    return by_id, by_name


def _infer_dark_threshold(path: str) -> float:
    by_id, by_name = _load_dark_thresholds()
    stem = Path(path).stem.lower()
    if stem.isdigit():
        return by_id.get(stem.zfill(3), 0.5)
    if "-" in stem:
        stem = stem.split("-")[0]
    return by_name.get(stem, 0.5)


def _palette_for_threshold(threshold: float):
    # High threshold means a bright image, so use darker text/palette.
    return LIGHT_BG_PALETTE if threshold >= 0.65 else DARK_BG_PALETTE


def _palette_for_path(path: str):
    text_mode = os.environ.get("POKEMON_TERMINAL_KITTY_TEXT_MODE", "auto").lower()
    if text_mode == "light":
        return DARK_BG_PALETTE
    if text_mode == "dark":
        return LIGHT_BG_PALETTE
    threshold = _infer_dark_threshold(path)
    return _palette_for_threshold(threshold)


def _cached_png_path(path: str) -> Path:
    src = Path(path)
    cache_root = Path.home() / ".cache" / "pokemon-terminal" / "kitty-images"
    cache_root.mkdir(parents=True, exist_ok=True)
    stat = src.stat()
    key = f"{src.resolve()}:{stat.st_mtime_ns}:{stat.st_size}"
    digest = sha1(key.encode("utf-8")).hexdigest()
    return cache_root / f"{digest}.png"


def _convert_to_png(path: str):
    src = Path(path)
    if src.suffix.lower() == ".png":
        return str(src)

    target = _cached_png_path(path)
    if target.exists():
        return str(target)

    with tempfile.NamedTemporaryFile(
        dir=str(target.parent), suffix=".png", delete=False
    ) as tmp:
        tmp_path = Path(tmp.name)

    try:
        if sys.platform == "darwin":
            run(["sips", "-s", "format", "png", str(src), "--out", str(tmp_path)],
                check=True, capture_output=True)
        else:
            run(["magick", str(src), str(tmp_path)], check=True, capture_output=True)
        tmp_path.replace(target)
        return str(target)
    except (CalledProcessError, OSError):
        tmp_path.unlink(missing_ok=True)
        return str(src)


class KittyProvider(_TProv):
    def is_compatible() -> bool:
        return "KITTY_WINDOW_ID" in os.environ

    def change_terminal(path: str):
        image_for_kitty = _convert_to_png(path)
        try:
            run(["kitty", "@", "set-background-image", image_for_kitty], check=True, capture_output=True)
        except CalledProcessError as err:
            print_kitty_error(err, "set background image")
            return

        palette = _palette_for_path(path)
        color_args = [f"{key}={value}" for key, value in palette.items()]
        try:
            run(["kitty", "@", "set-colors", *color_args], check=True, capture_output=True)
        except CalledProcessError as err:
            print_kitty_error(err, "set adaptive colors")

    def clear():
        try:
            run(["kitty", "@", "set-background-image", "none"], check=True, capture_output=True)
        except CalledProcessError as err:
            print_kitty_error(err, "clear background image")
        try:
            run(["kitty", "@", "set-colors", "--reset"], check=True, capture_output=True)
        except CalledProcessError as err:
            print_kitty_error(err, "reset colors")

    def __str__():
        return "Kitty"
