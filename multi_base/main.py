# coding: utf-8

"""
Main script for multi_base quepy.
"""

import quepy
dbpedia = quepy.install("multi_base")
target, query, metadata = dbpedia.get_query("what is a blowtorch?")
print query