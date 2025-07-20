#!/bin/sh

echo "Aplicando migrations com Alembic..."
alembic upgrade head

echo "Iniciando aplicação..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
