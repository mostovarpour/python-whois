import redis

redis_host = 'localhost'
redis_port = 6379
redis_password = ''

r = redis.StrictRedis(host=redis_host, port=redis_port,
                      password=redis_password, decode_responses=True)


def insert_ip_into_redis(query_in):
    try:
        r.set('key:ip', query_in)
    except Exception as e:
        print(e)

def insert_domain_into_redis(query_in):
    try:
        r.set('key:domain', query_in)
    except Exception as e:
        print(e)


def lookup_from_redis(domain):
    try:
        domain = r.get(domain)
        print(domain)
        return domain
    except Exception as e:
        print(e)


if __name__ == '__main__':
    insert_into_redis('test.com')
    lookup_from_redis('test.com')
