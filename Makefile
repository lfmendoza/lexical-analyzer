# Makefile for common development tasks

.PHONY: help install test lint format clean setup

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	poetry install
	poetry install --with dev

setup: ## Complete setup (install + pre-commit + test)
	poetry install
	poetry install --with dev
	poetry run pre-commit install
	poetry run pytest

test: ## Run tests
	poetry run pytest

test-cov: ## Run tests with coverage
	poetry run pytest --cov=lexical_analyzer --cov-report=html --cov-report=term

lint: ## Run linting
	poetry run flake8 . tests/
	poetry run mypy .

format: ## Format code
	poetry run black . tests/
	poetry run isort . tests/

format-check: ## Check code formatting
	poetry run black --check . tests/
	poetry run isort --check-only . tests/

pre-commit: ## Run pre-commit hooks
	poetry run pre-commit run --all-files

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run-example: ## Run example script
	poetry run python examples/example.py

run-cli: ## Run CLI with help
	poetry run lexical-analyzer --help

build: ## Build package
	poetry build

publish: ## Publish to PyPI (requires credentials)
	poetry publish

dev: ## Start development environment
	poetry shell

