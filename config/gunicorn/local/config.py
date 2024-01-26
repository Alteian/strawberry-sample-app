bind = "0.0.0.0:8000"  # Bind to all available interfaces on port 8000
workers = 1  # Number of workers based on the number of available CPU cores
worker_class = "uvicorn.workers.UvicornWorker"  # Use the Uvicorn worker class

preload_app = False  # Preload the app
timeout = 15  # Worker timeout in seconds

# Worker lifecycle settings
max_requests = 300  # Restart worker after processing 100 requests
max_requests_jitter = 50  # Add randomness to the max_requests setting to avoid workers restarting simultaneously
# Logging settings
accesslog = "-"  # stdout
errorlog = "-"  # stderr
loglevel = "debug"

# Reload settings (useful for development)
reload = True
reload_engine = "auto"
# reload_extra_files = []  # noqa: ERA001
