.PHONY: help install install-dev test test-verbose lint format clean coverage docs

help:			## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:		## Install package dependencies
	pip install -r requirements.txt

install-dev:		## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:			## Run tests
	python -m unittest discover tests

test-verbose:		## Run tests with verbose output
	python -m unittest discover tests -v

test-coverage:		## Run tests with coverage
	coverage run -m unittest discover tests
	coverage report
	coverage html

lint:			## Run linting tools
	flake8 telegram_nodes.py __init__.py
	black --check .
	isort --check-only .

format:			## Format code
	black .
	isort .

clean:			## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

docs:			## Generate documentation (placeholder)
	@echo "Documentation generation not implemented yet"

build:			## Build package
	python -m build

install-local:		## Install package locally in development mode
	pip install -e .

check-all:		## Run all checks (lint, test, coverage)
	make lint
	make test-coverage
