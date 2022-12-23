import json
import redis
from time import perf_counter_ns
from time import time


def lambda_handler(event, context):
    start = time()
    start_perf = perf_counter_ns()

    json_input = json.loads(event["body"])
    batch_size = json_input["batch_size"]
    redis_ip = json_input["redis"]
    redis_auth = json_input["password"]

    nodes = [redis.cluster.ClusterNode(host=redis_ip, port=7000 + port) for port in range(6)]
    c = redis.cluster.RedisCluster(host=redis_ip, password=redis_auth, port=7000, startup_nodes=nodes)

    image_keys = [key for key in c.keys(target_nodes=nodes)
                  if all([substring not in key for substring in ["FACE", "COLLAGE", "FIGURE"]])]  # get all keys of objects in redis cluster
    amt = int(len(image_keys)/batch_size+0.5)  # gets amount of sublists --> rounds up to next integer

    stop = perf_counter_ns()
    return {
        "keys": [image_keys[count::amt] for count in range(amt)],
        "start": start,
        "runtime": stop-start_perf
    }