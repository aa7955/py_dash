from collections import defaultdict
from datetime import datetime
from datetime import timedelta
from connection import redis_connection

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
        return {**self._time()}

def persistance_stats(conn_string):
    conn = redis_connection(conn_string)
    persistance_info = Persistance(conn)
    return persistance_info.print_stats()