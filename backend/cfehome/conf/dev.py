"""
Gunicorn development configuration file
"""
# This should not be used with a production server

# WSGI application path
wsgi_app = "cfehome.wsgi:application"

# Set log level to the lowest for development purposes
loglevel = "debug"

# Spawn 2 workers
workers = 2

# Bind to all ip addresses on port 8000
bind = "0.0.0.0:8008"

# Reload when any file is changed
reload = True

# our error and access log locations
access_log = error_log = "var/log/gunicorn/dev2.log"

# Redirect stderr/stdout to the log file
capture_output = True

# The location of our pid file
pidfile = "/var/run/gunicorn/dev.pid"

# We will daemonize this baby
daemon = True

