from memory import memory_stats
from persistance import persistance_stats
import pprint

redis_uri = "redis://localhost:6379"

mem = memory_stats(redis_uri)
pprint.pprint(mem)

per = persistance_stats(redis_uri)
pprint.pprint(per)

