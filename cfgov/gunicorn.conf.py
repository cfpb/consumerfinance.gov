import os


wsgi_app = "cfgov.wsgi:application"

bind = "0.0.0.0:8000"

accesslog = "-"

# All other settings default to gunicorn defaults if not set.
# See https://docs.gunicorn.org/en/latest/settings.html.

reload = bool(os.getenv("GUNICORN_RELOAD", False))

worker_class = os.getenv("GUNICORN_WORKER_CLASS", "sync")
workers = int(os.getenv("GUNICORN_WORKERS", 1))
worker_connections = int(os.getenv("GUNICORN_WORKER_CONNECTIONS", 1000))
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", 0))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", 0))

if worker_class == "gevent":
    from psycogreen.gevent import patch_psycopg

    def on_starting(server):
        patch_psycopg()
