#!/usr/bin/env python3
"""
task 10
"""


def update_topics(mongo_collection, name, topics):
    """
    change topic of colleciton in accordance to name
    """
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
