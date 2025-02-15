workers = 2
bind = "0.0.0.0:8000"
chdir = "/app/"
timeout = 300
module = "core.wsgi:application"
# worker_class = "gevent"
preload_app = True
worker_tmp_dir = "/dev/shm"
max_requests = 1000
max_requests_jitter = 50
keepalive = 60
loglevel = "debug"


