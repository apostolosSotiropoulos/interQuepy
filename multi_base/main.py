# coding: utf-8

"""
Main script for multi_base quepy.
"""

import quepy
multi_dbs = quepy.install("multi_base")
question = 'what is the sequel of a movie about giant monster staring' \
           ' Akira Takarada'
# question = 'what is a blowtorch?'
question = 'starring Akira Takarada'
# question = 'about Giant Monster'
# question = 'sequel of a movie'
target, query, metadata = multi_dbs.get_query(question)
print query
