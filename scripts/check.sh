set -euo pipefail

uv run ruff check 
uv run ruff format  
uv run mypy src tests
uv run pytest