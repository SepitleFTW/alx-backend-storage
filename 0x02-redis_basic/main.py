#!/usr/bin/env python3
"""
main project task
"""
import redis


Cache = __import__('exercise').Cache

cache = Cache()
cache.storage(b"first")
print(cache.get(cache.store.__qualname__))

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))
