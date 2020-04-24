import os

import redis
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = 'redis://localhost:6379'

conn = redis.from_url(redis_url)
with Connection(conn):
    worker = Worker(listen)
    worker.work()