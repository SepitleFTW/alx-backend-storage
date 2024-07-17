#!/usr/bin/env python3
"""
creating a Cache class in the __init__ method
store instance of redis cline as private var named _redis
(using redis.Redis()) then flushing using flushdb
Create a store method that takes a data argument and
returns a string. The method should generate a random
key (e.g. using uuid), store the input data in Redis
using the random key and return the key.
Type-annotate store correctly. Remember that
data can be a str, bytes, int or float.
"""
from functools import wraps
from typing import Any, Callable, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """
    tracking the no of calls made in cache class
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        returns method after incre its call counter
        """

        if isinstance(self._redis, redis.Redis):
            self.__redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    tracks the call dets of a metho in the cache class
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        returns the methods outpt after
        input and output is stored
        """
        int_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}"outputs'.format(method.__qualname__)
        if isinstance(self.__redis, redis.Redis):
            self.__redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self, _redis, redis.Redis):
            self.__redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    '''Displays history of call of cache class
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    '''cache class
    '''

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data:  Union[str, bytes, int, float]) -> str:
        '''stores data in redis.
        '''
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Retrieves a value from Redis .
        '''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''Retrieves a string value from Redis .
        '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Retrieves an integer value from Redis
        '''
        return self.get(key, lambda x: int(x))
