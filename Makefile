PYTHON ?= python3
VENV ?= .venv

PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
RUFF := $(VENV)/bin/ruff
BUILD := $(VENV)/bin/python -m build
TWINE := $(VENV)/bin/python -m twine
POKEMON := $(VENV)/bin/pokemon
PYTHON_VENV := $(VENV)/bin/python

.PHONY: setup lint test build package-check dry-run kitty-setup clean-venv

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

lint:
	@if [ ! -x "$(RUFF)" ]; then $(MAKE) setup; fi
	$(RUFF) check pokemonterminal tests scripts

test:
	@if [ ! -x "$(PYTEST)" ]; then $(MAKE) setup; fi
	$(PYTEST) -q

build:
	@if [ ! -x "$(PYTHON_VENV)" ]; then $(MAKE) setup; fi
	rm -rf dist build
	$(BUILD)

package-check:
	@if [ ! -x "$(PYTHON_VENV)" ]; then $(MAKE) setup; fi
	$(TWINE) check dist/*

dry-run:
	@if [ ! -x "$(POKEMON)" ]; then $(MAKE) setup; fi
	$(POKEMON) -dr

kitty-setup:
	@if [ ! -x "$(PYTHON_VENV)" ]; then $(MAKE) setup; fi
	$(PYTHON_VENV) scripts/kitty_setup.py

clean-venv:
	rm -rf $(VENV)
