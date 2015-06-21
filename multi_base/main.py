# coding: utf-8

"""
Main script for multi_base quepy.
"""

import quepy
multi_dbs = quepy.install("multi_base")
question = 'what is the sequel of a movie about giant monster staring' \
           ' Akira Takarada'
question2 = multi_dbs.get_query(question)
#target, query, metadata = multi_dbs.get_query("what is a blowtorch?")
print question
print question2
