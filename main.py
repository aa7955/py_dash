"""
PyDash is a Redis dashboard. It's not for production use and is solely used
as a learning tool for learning Python. Some of the comments in the code
are simply ideas that I have to create new features, or things that I 
don't want to forget to add or look at further (i.e. TODOs). This is definitely 
a work in progress. Disregard all shitty and non-standard code.
"""

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

class Memory:
    """
    Getting the memory stats from Redis.
    See https://redis.io/topics/memory-optimization for more information.
    Not all the stats from Redis INFO are represented here.

    If an instance exceeds the available memory, the OS will start swapping and
    old/unused sections of memory will be written to disk for newer memory sections.

    TODO:
    - Check if used_memory > total_system_memory to see if swapping has started.
    If so, send an alert - maybe change the text color here?
    """

    def __init__(self, connection):
        self.info = connection.info()

    def _memory(self):

        db_memory = defaultdict(int)

        # used memory - total bytes allocated by Redis
        db_memory['used_memory'] = self.info['used_memory']

        # memory rss (resident set memory) see memory allocation
        db_memory['rss_memory'] = self.info['used_memory_rss']

        # peak memory useage
        db_memory['memory_peak'] = self.info['used_memory_peak']

        # system memory used
        db_memory['sys_memory'] = self.info['total_system_memory']

        # RAM used
        db_memory['ram'] = self.info['maxmemory']

        return db_memory

    def print_stats(self):
        "prints the results from the memory function"
        print({**self._memory()})


class Persistance:

    """
    Getting the time stats from Redis. These might be updated in real-time.
    Need to figure out how much stress on the system this might have.
    """

    def __init__(self, connection):
        self.info = connection.info()

    def _time(self):

        db_time = defaultdict(str)

        saved_time = datetime.fromtimestamp(self.info['rdb_last_save_time'])
        formatted_time = saved_time.strftime('%b %d, %Y, %H:%M:%S')
        db_time['last_save_time'] = formatted_time

        db_time['uptime'] = timedelta(seconds=self.info['uptime_in_seconds'])

        return db_time

    def print_stats(self):
        "prints the results from the persistance function"
        print({**self._time()})


class Stats:

    """
    Have to figure out whether to merge all these classes together.
    Essentially, some of these would be updating themselves in real-time while
    others I am not entirely sure about. System stress for real-time statistics
    is something I need to figure out here.
    """

    def __init__(self, connection):
        self.info = connection.info()

    def _stats(self):
        """
        Mirrors the Stats section from Redis INFO
        """
        db_stats = defaultdict(int)

        db_stats['connections_received'] = self.info['total_connections_received'] 
        db_stats['commands_processed'] = self.info['total_commands_processed'] 
        db_stats['net_input_bytes'] = self.info['total_net_input_bytes'] 
        db_stats['net_output_bytes'] = self.info['total_net_output_bytes'] 
        db_stats['rejected_connections'] = self.info['rejected_connections']

        return db_stats

    def print_stats(self):
        "prints the results from the stats function"
        print({**self._stats()})


if __name__ == '__main__':
    client = client_connect(URL)
    stats = Stats(client)
    stats.print_stats()