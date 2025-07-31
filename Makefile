
# Default serve command (uses .env file)
serve:
	uv run -- python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Install dependencies
install:
	uv sync

check: 
	uv run ruff check

fix: 
	uv run ruff check --fix

migrate:
	uv run alembic revision --autogenerate -m "$(msg)"

# Manual migration (no autogenerate)
manual-migrate:
	uv run alembic revision -m "$(msg)"

upgrade: 
	uv run alembic upgrade head
	
