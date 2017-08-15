import redis


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


print "Testing"
conn = redis.Redis()
add_update_contact(conn, 'brunogs', 'Virginia')
add_update_contact(conn, 'brunogs', 'Nalva')
add_update_contact(conn, 'brunogs', 'Zeca')
print fetch_autocomplete_list(conn, 'brunogs', 'vir')
remove_contact(conn, 'brunogs', 'Virginia')
print conn.lrange('recent:brunogs', 0, -1)


