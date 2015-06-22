# coding: utf-8

"""
Domain specific language for multi_base quepy.
"""

from quepy.dsl import *

# classes used for basic dbpedia questions

# Setup the Keywords for this application
HasKeyword.relation = "rdfs:label"
HasKeyword.language = "en"

class DefinitionOf(FixedRelation):
    relation = "rdfs:comment"
    reverse = True


class IsPlace(FixedType):
    fixedtype = "dbpedia:Place"


class UTCof(FixedRelation):
    relation = "dbpprop:utcOffset"
    reverse = True


class LocationOf(FixedRelation):
    relation = "dbpedia-owl:location"
    reverse = True


# classes used for films


class IsSubject(FixedType):
    fixedtype = "skos:Concept"


class IsPerson(FixedType):
    fixedtype = "foaf:Person"


class IsSequel(HasKeyword):
    relation = "movie:sequel"

class SameAs(HasKeyword):
    relation = "owl:sameAs"

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


class HasSubject(FixedRelation):
    relation = "dcterms:subject"
