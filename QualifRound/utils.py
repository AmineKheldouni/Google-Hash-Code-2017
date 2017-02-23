#!/usr/bin/python
#encoding: utf8

import numpy as np
import math as m

def cost_request(requests, video_sizes, latency_cloud, endpointConnection):
    nb_endpoint = len(endpointConnection)
    nb_videos   = len(video_sizes)
    nb_cache = len(endpointConnection[0])
    print(nb_endpoint,nb_videos, nb_cache)
    cost_request_cache = np.zeros((nb_videos, nb_cache))
    for request in requests:
        video, endpoint , number = [int(i) for i in request]
        for cache in range(nb_cache):
            if endpointConnection[endpoint][cache] != m.inf:
                cost_request_cache[video][endpoint] += number*int(-endpointConnection[endpoint][cache]+latency_cloud\
                [endpoint])/video_sizes[video]
    return cost_request_cache
