import multiprocessing
import sys
import os
import gevent.monkey; gevent.monkey.patch_all()
import gunicorn
sys.path.append('./')

app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

backlog = 2048
max_requests = 20480
timeout = 1200  # master force kill children if children are unresponsive after this time
graceful_timeout = 60  # master force kill children after 300s when restarting
daemon = False
limit_request_line = 0
preload_app = False

user = 'root'
group = 'root'
workers = [NUM_WORKERS]
worker_class = "gevent"
worker_connections = 1024
#threads = 4
keepalive = 20
errorlog = '-'
accesslog='-' 
loglevel = "info"
bind = '0.0.0.0:[HOST_PORT]'

from gunicorn_settings import *
def post_fork(server, worker):
	import random
	random.seed()

