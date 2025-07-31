# ====================================================================================
# VARIABLES
# ====================================================================================

# Path to the Uvicorn application
MODULE_PATH ?= app.main:app
# Server configuration
SERVER_HOST ?= 0.0.0.0
SERVER_PORT ?= 8000
# Default Alembic migration message
MSG ?= "New migration"


# ====================================================================================
# PROJECT COMMANDS
# ====================================================================================

.PHONY: help
help: ##  Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ##  Install project dependencies using uv
	uv sync

.PHONY: run
run: ##  Run the development server (uses .env file)
	uv run -- uvicorn $(MODULE_PATH) --reload --host $(SERVER_HOST) --port $(SERVER_PORT)


# ====================================================================================
# CODE QUALITY & TESTING
# ====================================================================================

.PHONY: lint
lint: ## Check code for style and errors with Ruff
	uv run ruff check .

.PHONY: format
format: ## Automatically format code with Ruff
	uv run ruff check . --fix

.PHONY: test
test: ## Run automated tests (suggestion: configure your test command)
	# uv run pytest

.PHONY: all
all: lint format test ## Run all checks: lint, format, and test


# ====================================================================================
# DATABASE MIGRATIONS (ALEMBIC)
# ====================================================================================

.PHONY: db-migration
db-migration: ##   Generate a new database migration file (auto-detects changes)
	@if [ -z "$(msg)" ]; then echo "ERROR: Pass a message with 'make db-migration msg=\"your message\"'"; exit 1; fi
	uv run alembic revision --autogenerate -m "$(msg)"

.PHONY: db-migration-manual
db-migration-manual: ##   Generate a new empty migration file for manual editing
	@if [ -z "$(msg)" ]; then echo "ERROR: Pass a message with 'make db-migration-manual msg=\"your message\"'"; exit 1; fi
	uv run alembic revision -m "$(msg)"

.PHONY: db-upgrade
db-upgrade: ##  Apply all pending database migrations to the 'head'
	uv run alembic upgrade head

.PHONY: db-downgrade
db-downgrade: ##  Revert the last applied database migration (suggestion)
	uv run alembic downgrade -1


# ====================================================================================
# CLEANUP
# ====================================================================================

.PHONY: clean
clean: ##  Remove temporary Python files
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".ruff_cache" -delete