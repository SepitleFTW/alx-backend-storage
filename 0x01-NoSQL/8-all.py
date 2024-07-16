#!/usr/bin/env python3
"""task 8
"""


def list_all(mongo_collection):
    """
    show all docs
    """
    return [doc for doc in mongo_collection.find()]

