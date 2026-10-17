#!/bin/sh
if command -v uv >/dev/null; then
    exec uv run gunicorn app:server --workers 2 --bind "0.0.0.0:${PORT:-8000}"
else
    exec gunicorn app:server --workers 2 --bind "0.0.0.0:${POART:-8000}"
fi
