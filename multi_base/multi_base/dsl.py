# coding: utf-8

"""
Domain specific language for multi_base quepy.
"""

from quepy.dsl import FixedRelation

class IsDefinedIn(FixedRelation):
    relation = "rdfs:content"
    reverse = True