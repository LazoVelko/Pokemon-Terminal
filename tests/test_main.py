#!/usr/bin/env python3

# To run the tests, use: python3 -m pytest --capture=sys

from pokemonterminal.database import Database
from pokemonterminal.filters import Filter, RegionFilter, NonExtrasFilter
from pokemonterminal.main import main
from tests.test_utils import region_dict
import random

db = Database()


def broken_test_no_args(capsys):
    """ FIXME: Now the the main file accepts zero arguments """
    main([__file__])
    out, err = capsys.readouterr()
    assert out.startswith("No command line arguments specified.")


def broken_test_three_args(capsys):
    """ FIXME: Now the main file accepts way more then 3 arguments """
    main([__file__, 1, 2, 3])
    out, err = capsys.readouterr()
    assert out.startswith("Invalid number of arguments.")


def broken_test_two_letters(capsys):
    """ FIXME: The search argorhytm is now bultin the name filter """
    main([__file__, 'bu'])
    out, err = capsys.readouterr()
    assert 'Butterfree' in out
    # prefix search only
    main([__file__, 'ut'])
    out, err = capsys.readouterr()
    assert 'butterfree' not in out.lower()


def test_extra(capsys):
    main(['-e', '-dr'])
    # TODO: Assertion based on number of files on ./Extras
    assert str(random.choice(Filter.filtered_list)).startswith('---')


def test_region_names(capsys):
    try:
        main(['-r', 'wrong_region', '-dr'])
    except SystemExit:
        pass  # It's supposed to crash.
    err: str = capsys.readouterr()[1].strip()
    assert "argument -r/--region: invalid choice: 'wrong_region'" in err
    assert "choose from" in err
    for region in ('kanto', 'johto', 'hoenn', 'sinnoh', 'unova', 'kalos'):
        assert region in err


def test_all(capsys):
    main(['-dr', '-ne'])
    out = capsys.readouterr()[0]
    for region_info in region_dict.values():
        assert (region_info.first or '') in out  # convert None --> ''
        assert (region_info.last or '') in out   # convert None --> ''


def test_region(capsys):
    regFilter = RegionFilter(None, None)
    noExtras = NonExtrasFilter(None, None)
    # matrix test of first pokemon name and last pokemon name from all regions
    for name, region_info in region_dict.items():
        filtered = [p for p in Filter.POKEMON_LIST
                    if regFilter.matches(p, name)
                    and noExtras.matches(p, None)]
        assert len(filtered) == region_info.size
        assert random.choice(filtered).get_region() == name
        assert filtered[0].get_id() == ('%03d' % (region_info.start))
        assert filtered[-1].get_id() == ('%03d' % (region_info.end))
        assert filtered[0].get_name() == region_info.first.lower()
        assert filtered[-1].get_name() == region_info.last.lower()


if __name__ == '__main__':
    # Test runner: Runs all functions whose name begins with `test_`
    # locals() changes when trying to do this without the list comprehension!!!
    name_funcs = [(n, f) for n, f in locals().items() if n.startswith('test_')]
    for name, func in name_funcs:
        if callable(func):
            func()
        else:
            print(name + ' is not callable()!')
