"""
PyDash is a Redis dashboard. It's not for production use and is solely used
as a learning tool for learning Python. Some of the comments in the code
are simply ideas that I have to create new features, or things that I
don't want to forget to add or look at further (i.e. TODOs). This is definitely
a work in progress. Disregard all shitty and non-standard code.
"""

from urllib.parse import urlparse
import redis
import sys

class Connection:
    
    def __init__(self, conn_string):
        self.conn_string = conn_string

    def _redis_connection(self, conn_string):
        """
        - Set up a Redis Connection
        - Checking if the user supplies a valid Redis URI
        """
        
        if conn_string and (urlparse(conn_string).scheme == 'redis'):
            return redis.StrictRedis.from_url(conn_string)
        else:
            return "You need a Redis connection string to make this work!"
    
    def return_connection(self):
        try:
            conn = self._redis_connection(self.conn_string)
            return conn
        except Exception as e:
            print(e)


def redis_connection(conn_string):
    conn = Connection(conn_string)
    rconn = conn.return_connection()
    return rconn