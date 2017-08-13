import redis


def add_update_contact(conn, user, contact):
    ac_list = 'recent:' + user
    pipeline = conn.pipeline(True)
    pipeline.lrem(ac_list, contact)
    pipeline.lpush(ac_list, contact)
    pipeline.ltrim(ac_list, 0, 99)
    pipeline.execute()


print "Testing"
conn = redis.Redis()
add_update_contact(conn, 'brunogs', 'Virginia')
add_update_contact(conn, 'brunogs', 'Nalva')
add_update_contact(conn, 'brunogs', 'Zeca')
print conn.lrange('recent:brunogs', 0, -1)

