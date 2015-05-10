import unittest
import quepy


class TestFilmQuestions(unittest.TestCase):

    def setUp(self):
        self.app = quepy.install("multi_base")

    def test_query_generated_when_actor(self):
        # nl_question = 'Which movie is starring Akira Takarada'
        nl_question = 'starring Akira Takarada'
        expected_query = \
            u"""
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

            SELECT DISTINCT ?x2 WHERE {
            SERVICE <http://dbpedia.org/sparql> {
              ?x0 rdf:type dbpedia-owl:Film.
              ?x0 dbpprop:starring ?x1.
              ?x0 foaf:name ?x2.
              ?x1 rdf:type foaf:Person.
              ?x1 rdfs:label "Akira Takarada"@en.
            }
            }
            """

        target, query, userdata = self.app.get_query(nl_question)
        self.assertEqual(expected_query, query)

if __name__ == "__main__":
    unittest.main()
