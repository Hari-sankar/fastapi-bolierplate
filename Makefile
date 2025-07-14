serve:
	uv run -- python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

check: 
	uv run ruff check

fix: 
	uv run ruff check --fix
