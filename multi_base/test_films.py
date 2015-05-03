import unittest
import quepy


class TestFilmQuestions(unittest.TestCase):

    def setUp(self):
        self.app = quepy.install("multi_base")

    def test_query_generated_when_actor(self):
        nl_question = 'Which movie is starring Akira Takarada'
        expected_query = \
            u"""
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX dbpedia-owl:<http://dbpedia.org/ontology/>

            SELECT ?film_title WHERE {
                SERVICE <http://dbpedia.org/sparql> {
                    ?actor rdfs:label "Akira Takarada"@en .
                    ?dbpediaLink dbpedia-owl:starring ?actor .
                    ?dbpediaLink rdfs:label ?film_title
                }
            }
            """

        target, query, userdata = self.app.get_query(nl_question)
        self.assertEqual(expected_query, query)

if __name__ == "__main__":
    unittest.main()
