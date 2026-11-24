#!/usr/bin/env bash
set -e

echo "Executando migrations e seed inicial do SaaS..."
uv run alembic upgrade head

echo "Iniciando servidor FastAPI do SaaS..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload