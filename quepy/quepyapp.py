# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Implements the Quepy Application API
"""

from importlib import import_module
from types import ModuleType
from copy import deepcopy

from quepy import settings
from quepy.parsing import QuestionTemplate
from quepy.tagger import get_tagger
from quepy.encodingpolicy import encoding_flexible_conversion
from question import Question



def install(app_name):
    """
    Installs the application and gives an QuepyApp object
    """

    module_paths = {
        u"settings": u"{0}.settings",
        u"parsing": u"{0}",
    }
    modules = {}

    for module_name, module_path in module_paths.iteritems():
        try:
            modules[module_name] = import_module(module_path.format(app_name))
        except ImportError, error:
            message = u"Error importing {0!r}: {1}"
            raise ImportError(message.format(module_name, error))

    return QuepyApp(**modules)


def question_sanitize(question):
    question = question.replace("'", "\'")
    question = question.replace("\"", "\\\"")
    return question


class SplitString(object):
    """String that knows if, and can split by term"""

    whole_string = []
    substring_first = []
    substring_second = []
    is_rightmost = False

    def __init__(self, arg):
        self.whole_string = arg

    def can_be_split_by_term(self, term):
        try:
            index = self.whole_string.index(term)

            self.substring_first = SplitString(self.whole_string[0:index])
            self.substring_first.is_rightmost = self.is_rightmost

            self.substring_second = SplitString(self.whole_string[index:])
            self.substring_second.is_rightmost = True
        except Exception as e:
            return False
        return True


class QuepyApp(object):
    """
    Provides the quepy application API.
    """

    subquestions = []
    keywords = {}

    def __init__(self, parsing, settings):
        """
        Creates the application based on `parsing`, `settings` modules.
        """

        assert isinstance(parsing, ModuleType)
        assert isinstance(settings, ModuleType)

        self._parsing_module = parsing
        self._settings_module = settings

        # Save the settings right after loading settings module
        self._save_settings_values()

        self.tagger = get_tagger()
        self.dbURI = None
        self.language = getattr(self._settings_module, "LANGUAGE", None)
        if not self.language:
            raise ValueError("Missing configuration for language")

        self.rules = []
        for element in dir(self._parsing_module):
            element = getattr(self._parsing_module, element)

            try:
                if issubclass(element, QuestionTemplate) and \
                        element is not QuestionTemplate:

                    self.rules.append(element())
                    if hasattr(element(), 'keyword'):
                        self.keywords[element().keyword] = len(self.rules) - 1

            except TypeError:
                continue

        self.rules.sort(key=lambda x: x.weight, reverse=True)

    def get_query(self, nl_question):
        """
        Given `nl_question` in natural language, it returns
        three things:

        - the target of the query in string format
        - the query
        - metadata given by the regex programmer (defaults to None)

        The query returned corresponds to the first regex that matches in
        weight order.
        """

        nl_question = question_sanitize(nl_question)
        self.get_subquestions(nl_question.split(), self.keywords.keys())
        subquestions = self.subquestions if self.subquestions else nl_question

        question = Question(subquestions, self.rules, self.keywords)
        return question.get_query()



    def _save_settings_values(self):
        """
        Persists the settings values of the app to the settings module
        so it can be accesible from another part of the software.
        """

        for key in dir(self._settings_module):
            if key.upper() == key:
                value = getattr(self._settings_module, key)
                if isinstance(value, str):
                    value = encoding_flexible_conversion(value)
                setattr(settings, key, value)

    def get_subquestions(self, words, keywords):
        """ input:
                ['hello', 'keyword1', 'is', 'foo', 'keyword2', 'is', 'bar'] and
                ['keyword1', 'keyword2']
            output:
                [['keyword1', 'is', 'foo'], ['keyword2', 'is', 'bar']]"""

        sstring = SplitString(words) if type(words) is list else words

        if len(keywords) == 0:
            return 42
        keywords_copy = deepcopy(keywords)
        keyword = keywords_copy.pop()

        if sstring.can_be_split_by_term(keyword) :
            second_substring = sstring.substring_second
            if self.get_subquestions(second_substring, keywords_copy) == 42:
                self.subquestions.append(second_substring.whole_string)

            first_substring = sstring.substring_first
            if self.get_subquestions(first_substring, keywords_copy) == 42 and \
                first_substring.is_rightmost:
                    self.subquestions.append(first_substring.whole_string)
        else :
            return self.get_subquestions(words, keywords_copy)
