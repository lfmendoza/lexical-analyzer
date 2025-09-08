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
	poetry run pytest --cov=src/lexical_analyzer --cov-report=html --cov-report=term

lint: ## Run linting
	poetry run flake8 src/ tests/
	poetry run mypy src/

format: ## Format code
	poetry run black src/ tests/
	poetry run isort src/ tests/

format-check: ## Check code formatting
	poetry run black --check src/ tests/
	poetry run isort --check-only src/ tests/

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

