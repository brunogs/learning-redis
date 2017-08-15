import redis
import bisect
import uuid


def add_update_contact(conn, user, contact):
    ac_list = 'recent:' + user
    pipeline = conn.pipeline(True)
    pipeline.lrem(ac_list, contact)
    pipeline.lpush(ac_list, contact)
    pipeline.ltrim(ac_list, 0, 99)
    pipeline.execute()

def remove_contact(conn, user, contact):
    conn.lrem('recent:' + user, contact)

def fetch_autocomplete_list(conn, user, prefix):
    candidates = conn.lrange('recent:' + user, 0, -1)
    matches = []
    for candidate in candidates:
        if candidate.lower().startswith(prefix):
            matches.append(candidate)
    return matches


valid_characters = '`abcdefghijklmnopqrstuvwxyz{'

def find_prefix_range(prefix):
    posn = bisect.bisect_left(valid_characters, prefix[-1:])
    suffix = valid_characters[(posn or 1) - 1]
    return prefix[:-1] + suffix + '{', prefix + '{'


def autocomplete_on_prefix(conn, guild, prefix):
    start, end = find_prefix_range(prefix)
    identifier = str(uuid.uuid4())
    start += identifier
    end += identifier
    zset_name = 'members:' + guild

    conn.zadd(zset_name, start, 0, end, 0)
    pipeline = conn.pipeline(True)
    while 1 :
        try:
             pipeline.watch(zset_name)
             sindex = pipeline.zrank(zset_name, start)
             eindex = pipeline.zrank(zset_name, end)
             erange = min(sindex + 9, eindex - 2)
             pipeline.multi()
             pipeline.zrem(zset_name, start, end)
             pipeline.zrange(zset_name, sindex, erange)
             items = pipeline.execute()[-1]
             break
        except redis.exceptions.WatchError:
            continue
    return [item for item in items if '{' not in item]


print "Testing"
conn = redis.Redis()
add_update_contact(conn, 'brunogs', 'Virginia')
add_update_contact(conn, 'brunogs', 'Nalva')
add_update_contact(conn, 'brunogs', 'Zeca')
print fetch_autocomplete_list(conn, 'brunogs', 'vir')
remove_contact(conn, 'brunogs', 'Virginia')
print conn.lrange('recent:brunogs', 0, -1)


print find_prefix_range('Vir')

