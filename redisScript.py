import redis
import random

# redis connection --> change host
r = redis.Redis(host=input("Enter Host: "), port=6379, db=0, password=input("Enter Password: "))

# sets 10 random entries
for i in range(10):
    r.set(random.randbytes(15), f"entry_{i}")


# get values by key
def retrieve_entry(keys) -> list:
    values = []
    for key in keys:
        print(key)
        values.append(r.get(key))
    return values


def del_all(keys):
    for key in keys:
        r.delete(key)


# retrieves all keys on redis cluster
keys = r.scan_iter()

print(f"Values: {retrieve_entry(keys=keys)}")
print(f"Keys: {' '.join(map(str,keys))}")

del_all(keys=keys)


