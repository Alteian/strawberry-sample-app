#!/bin/bash

exec $(which gunicorn) -c /app/config/gunicorn/prod/config.py src.asgi:application
