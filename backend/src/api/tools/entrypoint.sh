#!/bin/sh

# Start Uvicorn with live reload, excluding /proc
exec poetry run uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload --reload-dir /api