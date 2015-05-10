# coding: utf-8

"""
Domain specific language for multi_base quepy.
"""

from quepy.dsl import FixedDataRelation, FixedType, FixedRelation


class IsPerson(FixedType):
    fixedtype = "foaf:Person"


class LabelOf(FixedDataRelation):
    relation = "rdfs:label"
    language = "en"
    reverse = True


class NameOf(FixedRelation):
    relation = "foaf:name"
    # relation = "dbpprop:name"
    reverse = True


class IsMovie(FixedType):
    fixedtype = "dbpedia-owl:Film"


class HasActor(FixedRelation):
    relation = "dbpprop:starring"
