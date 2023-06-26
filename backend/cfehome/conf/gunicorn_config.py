wsgi_app = 'cfehome.wsgi:application'

command = '/home/jesse/Projects/DRF/env/bin/gunicorn'

pythonpath = '/home/jesse/Projects/DRF/backend/cfehome'

bind = '0.0.0.0:8008'

workers = 3

reload = True

accesslog = errorlog = "/var/log/gunicorn/dev2.log"

timeout = 3600

graceful_timeout = 3600

capture_output = True

loglevel = "debug"

pidfile = '/var/run/gunicorn/gunicorn_dev.pid'

daemon = True
