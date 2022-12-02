import redis

# redis connection --> change host
r = redis.Redis(host='localhost', port=6379, db=0, password="insert")


# get values by key
def retrieve_entry(keys: list) -> list:
    values = []
    for key in keys:
        values.append(r.get(key))
    return values


# sets 10 random entries
for i in range(10):
    r.set(id(i), f"entry_{i}")

# retrives all keys on redis cluster
keys = r.scan_iter()


