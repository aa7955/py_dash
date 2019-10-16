import collections
from connection import redis_connection
import pprint

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

        db_memory = collections.defaultdict(int)

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
        return {**self._memory()}

def memory_stats(conn_string):
    conn = redis_connection(conn_string)
    mem_info = Memory(conn)
    return mem_info.print_stats()