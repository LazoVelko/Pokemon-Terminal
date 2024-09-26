import sys as sys
import argparse
import pokemonterminal.filters as filters
from pokemonterminal.database import Database


parser = argparse.ArgumentParser(
    description='Set a pokemon to the current terminal background or '
    'wallpaper',
    epilog='Not setting any filters will get a completely random pokemon')

_filters_group = parser.add_argument_group(
    'Filters', 'Arguments used to filter the list of pokemons with '
    'various conditions that then will be picked')
_filters_group.add_argument(
    '-n',
    '--name',
    help='Filter by pokemon which name contains NAME',
    action=filters.NameFilter,
    type=str.lower)
_filters_group.add_argument(
    '-r',
    '--region',
    help='Filter the pokemons by region',
    action=filters.RegionFilter,
    choices=Database.REGIONS,
    nargs='*',
    type=str.lower)
_filters_group.add_argument(
    '-l',
    '--light',
    help='Filter out the pokemons darker (lightness threshold lower) ' +
    'then 0.xx (default is 0.7)',
    default=0.7,
    const=0.7,
    metavar='0.xx',
    nargs='?',
    type=float,
    action=filters.LightFilter)
_filters_group.add_argument(
    '-d',
    '--dark',
    help='Filter out the pokemons lighter (lightness threshold higher) ' +
    'then 0.xx (default is 0.42)',
    default=0.42,
    const=0.42,
    metavar='0.xx',
    nargs='?',
    type=float,
    action=filters.DarkFilter)
_filters_group.add_argument(
    '-t',
    '--type',
    help='Filter the pokemons by type.',
    action=filters.TypeFilter,
    choices=Database.POKEMON_TYPES,
    nargs='*',
    type=str.lower)
_filters_group.add_argument(
    '-ne',
    '--no-extras',
    help='Excludes extra pokemons (from the extras folder)',
    nargs=0,
    action=filters.NonExtrasFilter)
_filters_group.add_argument(
    '-e',
    '--extras',
    help='Excludes all non-extra pokemons',
    nargs=0,
    action=filters.ExtrasFilter)

_misc_group = parser.add_argument_group("Misc")
_misc_group.add_argument(
    '-ss',
    '--slideshow',
    help='Instead of simply choosing a random pokemon ' +
    'from the filtered list, starts a slideshow (with X minutes ' +
    'of delay between pokemon) in the background with the ' +
    'pokemon that matched the filters',
    const=10.0, nargs='?', type=float, metavar='X')


is_slideshow = '-ss' in sys.argv or '--slideshow' in sys.argv
_misc_group.add_argument(
    '-w',
    '--wallpaper',
    help='Changes the desktop wallpaper instead of the terminal '
    'background',
    action='store_true')
_misc_group.add_argument(
    '-v', '--verbose', help='Enables verbose output', action='store_true')
_misc_group.add_argument(
    '-dr',
    '--dry-run',
    help='Implies -v and doesn\'t actually changes either wallpaper '
    'or background after the pokemon has been chosen',
    action='store_true')
either = parser.add_mutually_exclusive_group()
either.add_argument(
    '-c',
    '--clear',
    help='Clears the current pokemon from terminal '
    'background and quits.',
    action='store_true')
either.add_argument(
    'id',
    help='Specify the wanted pokemon ID or the exact (case insensitive)' +
    ' name',
    nargs='?',
    default=0, const=0)
either.add_argument(
    '--list',
    help='list all pokemons',
    action='store_true')
