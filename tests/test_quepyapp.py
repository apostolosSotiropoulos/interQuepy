#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Tests for QuepyApp.
"""

import unittest

import quepy


class TestQuepyApp(unittest.TestCase):

    def setUp(self):
        self.app = quepy.install("testapp")

    def test_get_query_types(self):
        question = "What is this?"
        target, query, userdata = self.app.get_query(question)

        self.assertIsInstance(target, unicode)
        self.assertIsInstance(query, unicode)

    def test_get_user_data(self):
        question = "user data"
        target, query, userdata = self.app.get_query(question)
        self.assertEqual(userdata, "<user data>")

    def test_priority(self):
        question = "something something"
        target, query, userdata = self.app.get_query(question)
        self.assertEqual(userdata, 42)

    def test_config_is_saved(self):
        from quepy import settings
        self.assertIn("testapp", settings.SPARQL_PREAMBLE)

    def test_set_metadata_when_list_given(self):
        metadata = ['enum', u'<http://dbpedia.org/sparql>']
        self.app._set_metadata(metadata)
        self.assertEqual('enum', self.app.userdata)
        self.assertEqual(u'<http://dbpedia.org/sparql>', self.app.dbURI)

    def test_set_metadata_when_string_given(self):
        metadata = 'enum'
        self.app._set_metadata(metadata)
        self.assertEqual('enum', self.app.userdata)
        self.assertIsNone(self.app.dbURI)

    def test_get_subquestions_when_no_keywords_matched(self):
        question = 'what is the sequel of a movie about giant monster staring' \
                   ' Akira Takarada'
        keywords = ['foo']

        expected_subquestions = []
        self.app.get_subquestions(question.split(), keywords)
        self.assertEqual(expected_subquestions, self.app.subquestions)

    def test_get_subquestions_when_keywords_in_all_possible_orders(self):
        k1 = 'sequel'
        k2 = 'about'
        k3 = 'staring'

        self._get_subquestions_when_keywords_in_order(k1, k2, k3)
        self._get_subquestions_when_keywords_in_order(k1, k3, k2)
        self._get_subquestions_when_keywords_in_order(k2, k1, k3)
        self._get_subquestions_when_keywords_in_order(k2, k3, k1)
        self._get_subquestions_when_keywords_in_order(k3, k1, k2)
        self._get_subquestions_when_keywords_in_order(k3, k2, k1)

    def _get_subquestions_when_keywords_in_order(self, k1, k2, k3):
        question = 'what is the sequel of a movie about giant monster staring' \
                   ' Akira Takarada'
        keywords = ['keyword1', k1, 'keyword2', k2, 'keyword3',
                    k3,'keyword4']

        expected_subquestions = [
            'staring Akira Takarada'.split(),
            'about giant monster'.split(),
            'sequel of a movie'.split()
        ]
        self.app.get_subquestions(question.split(), keywords)
        self.assertEqual(expected_subquestions, self.app.subquestions)
        self.app.subquestions = []

if __name__ == "__main__":
    unittest.main()
