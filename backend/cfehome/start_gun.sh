#! /bin/bash

source /home/jesse/DRF/env/bin/activate &&

cd /home/jesse/DRF/backend/cfehome &&

echo "[Killing Gunicorn]"
killall gunicorn

echo "[Restarting Gunicorn]"
gunicorn -c /home/jesse/DRF/backend/cfehome/conf/gunicorn_config.py cfehome.wsgi