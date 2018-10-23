import redis

redis_host = 'localhost'
redis_port = 6379
redis_password = ''

r = redis.StrictRedis(host=redis_host, port=redis_port,
                      password=redis_password, decode_responses=True)


def insert_ip_into_redis(query_in):
    try:
        r.set(query_in, query_in)
    except Exception as e:
        print(e)


def insert_domain_into_redis(query_in):
    try:
        r.set(query_in, query_in)
    except Exception as e:
        print(e)


def lookup_from_redis(query_in):
    try:
        keys = r.keys(query_in)
        for key in keys:
            type = r.type(key)
            val = r.get(key)
            return val
    except Exception as e:
        print(e)




if __name__ == '__main__':
    insert_ip_into_redis('10.0.0.3')
    insert_domain_into_redis('test.com')
    result = lookup_from_redis('test.com')
    print(result)

    # ips = r.scan('keys:ip')
    # for i in ips:
    #     print i