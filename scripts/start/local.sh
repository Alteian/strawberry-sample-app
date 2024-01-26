#!/bin/bash

echo "Starting local server..."

exec $(which gunicorn) -c /app/config/gunicorn/local/config.py src.asgi:application
