from os import environ
from subprocess import run, DEVNULL
from . import WallpaperProvider as _WProv
from shutil import which

class HyprlandProvider(_WProv):
    def change_wallpaper(path: str):
        run(["hyprctl", "hyprpaper", "preload", path], stdout=DEVNULL, check=True)

        run(["hyprctl", "hyprpaper", "wallpaper", ","+path], stdout=DEVNULL, check=True)

    def is_compatible() -> bool:
        tools_available = which("hyprctl") is not None and which("hyprpaper") is not None
        de_is_hypr = "hyprland" in environ.get("XDG_CURRENT_DESKTOP", default='').lower()

        return tools_available and de_is_hypr

    def __str__():
        return "Hyprland wallpaper support"
