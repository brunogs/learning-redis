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


print "Testing"
conn = redis.Redis()
add_update_contact(conn, 'brunogs', 'Virginia')
add_update_contact(conn, 'brunogs', 'Nalva')
add_update_contact(conn, 'brunogs', 'Zeca')
print conn.lrange('recent:brunogs', 0, -1)
remove_contact(conn, 'brunogs', 'Virginia')
print conn.lrange('recent:brunogs', 0, -1)


