#!/bin/bash

exec $(which gunicorn) -c /app/config/gunicorn/dev/config.py src.asgi:application
