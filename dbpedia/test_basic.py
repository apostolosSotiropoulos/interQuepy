import unittest
import quepy

class TestBasicQuestions(unittest.TestCase):

    def setUp(self):
        self.app = quepy.install("dbpedia")

    def test_query_generated_when_what_is_blowtorch(self):
        nl_question = 'what is a blowtorch'
        expected_query = u'\nPREFIX owl: <http://www.w3.org/2002/07/owl#>\n' \
                         u'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n' \
                         u'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n' \
                         u'PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n' \
                         u'PREFIX skos: <http://www.w3.org/2004/02/skos/core#>\n' \
                         u'PREFIX quepy: <http://www.machinalis.com/quepy#>\n\n' \
                         u'SELECT DISTINCT ?x1 WHERE {\n' \
                         u'  ?x0 quepy:Keyword "blowtorch".\n' \
                         u'  ?x0 rdfs:content ?x1.\n' \
                         u'}\n'

        target, query, userdata = self.app.get_query(nl_question)
        self.assertEqual(expected_query, query)

if __name__ == "__main__":
    unittest.main()
