# adding something here
# adding something else



from memory import memory_stats
from persistance import persistance_stats
from stats import get_stats
import pprint

redis_uri = "redis://localhost:6379"

mem = memory_stats(redis_uri)
pprint.pprint(mem)

per = persistance_stats(redis_uri)
pprint.pprint(per)

stats = get_stats(redis_uri)
pprint.pprint(stats)
