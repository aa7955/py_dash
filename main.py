from urllib.parse import urlparse
from datetime import datetime, timedelta
from collections import defaultdict
import redis
import os
import sys

URL = ""

if sys.argv[1] and (urlparse(sys.argv[1]).scheme == 'redis'):
        URL = sys.argv[1]
else:
    print("You need a Redis connection string to make this work!")

def client_connect(url):
    "parse the connection string and connect to redis"

    parsed_url = urlparse(url)
    connection_pool = redis.StrictRedis(
        host = parsed_url.hostname,
        port = parsed_url.port,
        password = parsed_url.password,
        decode_responses=True)

    return connection_pool

class Stats:
    "responsible for exposing the info that's needed from Redis"

    def __init__(self, connection):
        conn = connection
        self.info = conn.info()

    def _memory(self):
        "getting the memory stats from Redis"
        db_memory = defaultdict(int)

        db_memory['sys_memory'] = self.info['total_system_memory'] # system memory
        db_memory['ram'] = self.info['maxmemory'] # ram 

        return db_memory

    def _time(self):
        "getting the time stats from redis"
        db_time = defaultdict(str)

        saved_time = datetime.fromtimestamp(self.info['rdb_last_save_time'])
        formatted_time = saved_time.strftime('%b %d, %Y, %H:%M:%S')
        db_time['last_save_time'] = formatted_time

        db_time['uptime'] = timedelta(seconds = self.info['uptime_in_seconds'])

        return db_time

    def print_stats(self):
        "prints the results from the stats functions"
        print({**self._memory(), **self._time()})


if __name__ == '__main__':
    client = client_connect(URL)
    stats = Stats(client)
    stats.print_stats()