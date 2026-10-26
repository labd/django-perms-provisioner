.PHONY: install test retest coverage lint format release


install:
	uv sync

test:
	uv run pytest

retest:
	uv run pytest -vvv --lf

coverage:
	uv run pytest --cov=django_perms_provisioner --cov-report=term-missing --cov-report=html

lint:
	uv run ruff format --check src tests
	uv run ruff check src tests

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

release:
	rm -rf dist/*
	uv build
