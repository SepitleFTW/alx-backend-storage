#!/usr/bin/env python3
"""
task9
"""


def insert_school(mongo_collection, **kwargs):
    """
    put in new doc in collection
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
