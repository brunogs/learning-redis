import redis
import time

def create_user(conn, login, name):
    login = login.lower()
    #TODO add lock functions
    # lock = acquire_lock_with_timeout(conn, 'user:' + login, 1)
    #if not lock:
    #    return None

    if conn.hget('users:', login):
        return None

    id = conn.incr('user:id:')
    pipeline = conn.pipeline(True)
    pipeline.hset('users:', login, id)
    pipeline.hmset('users:%s'%id, {
        'login': login,
        'name': name,
        'followers': 0,
        'following': 0,
        'posts': 0,
        'signup': time.time(),
    })
    pipeline.execute()
    #TODO add lock functions
    # release_lock(conn, 'user:' + login, lock)
    return id


def cleanup(conn, keyPattern):
    for key in conn.keys(keyPattern):
        conn.delete(key)


print 'Simple Tests\n'
conn = redis.Redis()
cleanup(conn, '*users:*')

print 'Should create an user'
user_id = create_user(conn, 'btuttin', 'Bruno Silva')
print 'user created with id=%s'%user_id
print conn.hgetall('users:%s'%user_id)
