#!/bin/bash --login
# This entrypoint is used primarily as means of setting up a consistent
# shell environment no matter which user the process runs as.  By using
# --login, it guarantees /etc/profile is always sourced, unlike the
# non-login, non-interactive shell you get by default with `docker run`.

exec "$@"
