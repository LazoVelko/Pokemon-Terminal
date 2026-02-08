#!/usr/bin/env python3
"""The main module that brings everything together."""

import random
import sys

from . import scripter, slideshow
from pokemonterminal.command_flags import parser, is_slideshow
from pokemonterminal.database import Database
from pokemonterminal.filters import Filter
from pokemonterminal.platform import PlatformNamedEvent



def main(argv=None):
    """Entrance to the program."""
    if __name__ != "__main__":
        Filter.filtered_list = [pok for pok in Filter.POKEMON_LIST]
    # TODO Lower main() complexity with factory functions or something
    options = parser.parse_args(argv)  # Parser is imported at top of file.
    try:
        options.id = int(options.id)
    except ValueError:
        options.name = options.id.lower()
        options.id = 0
        Filter.filtered_list = [
            x for x in Filter.filtered_list if options.name == x.get_name()
        ]

    size = len(Filter.filtered_list)
    if size == 0:
        print("No pokemon matches the specified filters")
        return

    if options.id <= 0:
        # TODO this doesn't account for the current set pokemon and might try
        # TODO to set the same pokemon again (essentially not doing anything)
        target = random.choice(Filter.filtered_list)
    else:
        options.id -= 1
        if len(Filter.POKEMON_LIST) > options.id:
            if len(sys.argv) > 2:
                print("ID has been specified, ignoring all filters.")
            size = 1
            target = Filter.POKEMON_LIST[options.id]
            Filter.filtered_list = [target]
        else:
            print("Invalid id specified")
            return

    if options.verbose or options.dry_run:
        if size == 1:
            print('A single pokemon matches the specified criteria: ')
        if size > Database.MAX_ID:
            print('No pokemon has been filtered...')
        else:
            # Print the list of filtered pokemon
            [
                print(f"#{pkmn.get_id()} - {pkmn.get_name().title()}")
                for pkmn in Filter.filtered_list
            ]
        print("Total of %d pokemon matched the filters. Chose %s" %
              (size, target.get_name().title()))

    if options.dry_run:
        print("Dry run, exiting.")
        return

    event_name = "Pokemon-Terminal_Wallpaper" if options.wallpaper else "Pokemon-Terminal_Terminal"
    event_exists = PlatformNamedEvent.exists(event_name)

    if options.clear:
        if event_exists:
            slideshow.stop(event_name)
        if not options.wallpaper:
            scripter.clear_terminal()
        return

    if is_slideshow and options.id <= 0 and size > 1:
        if options.slideshow <= 0:
            print("Time has to be greater than 0. You can use decimal values.")
            return
        if event_exists:
            print("One or more slideshows is already running.\n")
            while True:
                print("[S]top the previous slideshow(s) / ", end='')
                if not options.wallpaper:
                    print("[I]gnore and continue / ", end='')
                print("[A]bort")
                inp = input("Pick one: ").lower()
                if inp == 's':
                    slideshow.stop(event_name)
                    break
                elif inp == 'i' and not options.wallpaper:
                    break
                elif inp == 'a':
                    return
                else:
                    print("Not a valid option!\n")
        target_func = scripter.change_wallpaper if options.wallpaper else scripter.change_terminal
        print(f"Starting slideshow with {len(Filter.filtered_list)} Pokemons and a delay of {options.slideshow} minutes.")
        pid = slideshow.start(Filter.filtered_list, options.slideshow, target_func, event_name)
        print(f"Forked process to background with PID {pid}.")
        print("You can stop it with 'pokemon {}'.".format('-c -w' if options.wallpaper else '-c'))
        return

    if options.wallpaper:
        scripter.change_wallpaper(target.get_path())
    else:
        scripter.change_terminal(target.get_path())


if __name__ == "__main__":
    # Entrance to the program.
    main(sys.argv[1:])
