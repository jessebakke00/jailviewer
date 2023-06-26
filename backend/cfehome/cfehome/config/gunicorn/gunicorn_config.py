"""Gunicor *development* config file"""

# Django WSGI application path in pattern
wsgi_app = "cfehome.wsgi:application"

# The granularity of Error log outputs
loglevel = "debug"

# Number of workers
workers = 2

# Socket to bind to
bind = "0.0.0.0:8000"

# restart workers when code changes
reload = True

# Write access and error logs 
accesslog = errorlog = "var/log/gunicorn/dev.log"

# Redirect stdout/stder to log file
capture_output = True

# PID FILE
pidfile = "/var/run/gunicorn/dev.pid"

# Daemonize the Gunicorn process
daemon = True
