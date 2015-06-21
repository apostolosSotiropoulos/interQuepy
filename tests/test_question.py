import unittest

import quepy
from quepy.question import Subquestion


class TestSubquestion(unittest.TestCase):
    def setUp(self):
        multi_dbs = quepy.install("testapp")
        self.subqueries = [
            {'db': 'http://dbpedia.org/sparql',
             'query': u"""\
                ?x0 rdf:type foaf:Person.
                ?x0 rdfs:label "Akira Takarada"@en.
                ?movie rdf:type dbpedia-owl:Film.
                ?movie dbpprop:starring ?x0.
            """},
            {'db': 'http://dbpedia.org/sparql',
             'query': u"""\
                ?x20 rdf:type skos:Concept .
                ?x20 rdfs:label "Giant monster films"@en .
                ?movie rdf:type dbpedia-owl:Film .
                ?movie dcterms:subject ?subject .
            """},
            {'db': 'http://data.linkedmdb.org/sparql',
             'query': u"""
                ?x30 owl:sameAs ?movie.
                ?x30 movie:sequel ?movie2 .
            """},
            {'db': 'http://data.linkedmdb.org/sparql',
             'query': u"""
                ?movie2 rdfs:label ?output.
            """}]

        self.subquestion = \
            Subquestion(self.subqueries, multi_dbs.rules)

    def test_merge_subqueries(self):
        expected_query = u"""
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX quepy: <http://www.machinalis.com/quepy#>
            PREFIX dbpedia: <http://dbpedia.org/ontology/>
            PREFIX dbpprop: <http://dbpedia.org/property/>
            PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
            PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
            PREFIX dcterms: <http://purl.org/dc/terms/>


            SELECT ?output ?subject WHERE {
                SERVICE <http://dbpedia.org/sparql> {
                    ?x0 rdf:type foaf:Person.
                    ?x0 rdfs:label "Akira Takarada"@en.
                    ?movie rdf:type dbpedia-owl:Film.
                    ?movie dbpprop:starring ?x0.
                    ?x20 rdf:type skos:Concept .
                    ?x20 rdfs:label "Giant monster films"@en .
                    ?movie rdf:type dbpedia-owl:Film .
                    ?movie dcterms:subject ?subject .
                }
                SERVICE <http://data.linkedmdb.org/sparql> {
                    ?x30 owl:sameAs ?movie.
                    ?x30 movie:sequel ?movie2 .
                    ?movie2 rdfs:label ?output.
                }
            }"""

        query = self.subquestion._merge_subqueries(self.subqueries)
        self.assertEqual(expected_query, query)
