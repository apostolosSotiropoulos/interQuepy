# coding: utf-8

"""
Main script for dbpedia quepy.
"""

import quepy
dbpedia = quepy.install("dbpedia")
target, query, metadata = dbpedia.get_query("what is a blowtorch?")
print query