from urllib.parse import urlparse
from datetime import datetime, timedelta
from collections import defaultdict
import redis
import argparse
import os

URL = os.environ['REDIS']

def client_connect(url):
    """connect to redis"""
    parsed = urlparse(url)
    connect = redis.StrictRedis(
        host=parsed.hostname,
        port=parsed.port,
        password=parsed.password,
        decode_responses=True)

    return connect

def get_info(red):
    """accesses redis info after client_connect"""
    return red.info()

def memory(info):
    """getting the memory stats from Redis"""
    db_display_info = defaultdict(int)
    # system memory
    db_display_info['sys_memory'] = info['total_system_memory']
    # system ram
    db_display_info['ram'] = info['maxmemory']

    return db_display_info

def time(info):
    """getting the time stats from redis"""
    db_time = defaultdict(str)
    # last saved time 
    db_time['last_save_time'] = datetime.fromtimestamp(info['rdb_last_save_time']).strftime("%b %d, %Y, %H:%M:%S")
    # uptime in seconds
    db_time['uptime'] = timedelta(seconds=info['uptime_in_seconds'])
    return db_time


if __name__ == '__main__':
    conn = client_connect(URL)
    info = get_info(conn)
    print(memory(info))
    print(time(info))