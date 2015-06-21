import logging

from quepy import settings
from quepy import generation
from quepy.tagger import get_tagger, TaggingError
from quepy.encodingpolicy import encoding_flexible_conversion

logger = logging.getLogger("quepy.quepyapp")


class Question():
    def __init__(self, subquestions, rules):
        self.subquestions = subquestions
        self.rules = rules

    def get_query(self):
        if type(self.subquestions) is list:
            question = Subquestion(self.subquestions, self.rules)
        else:
            question = FullQuestion(self.subquestions, self.rules)
        return question.get_query()


class FullQuestion(Question):
    """docstring for FullQuestion"""
    def get_query(self):
        """
        Given `question` in natural language, it returns
        three things:

        - the target of the query in string format
        - the query
        - metadata given by the regex programmer (defaults to None)

        The queries returned corresponds to the regexes that match in
        weight order.
        """
        question = encoding_flexible_conversion(self.subquestions)
        for expression, metadata in self._iter_compiled_forms(question):
            target, query = generation.get_code(expression, settings.LANGUAGE)
            message = u"Interpretation {1}: {0}"
            logger.debug(message.format(str(expression),
                         expression.rule_used))
            logger.debug(u"Query generated: {0}".format(query))
            return target, query, metadata

    def _iter_compiled_forms(self, question):
        """
        Returns all the compiled form of the question.
        """
        try:
            tagger = get_tagger()
            words = list(tagger(question))
        except TaggingError:
            logger.warning(u"Can't parse tagger's output for: '%s'",
                           question)
            return

        logger.debug(u"Tagged question:\n" +
                     u"\n".join(u"\t{}".format(w for w in words)))

        for rule in self.rules:
            expression, userdata = rule.get_interpretation(words)
            if expression:
                yield expression, userdata

    def _set_metadata(self, metadata):
        try:
            self.userdata, self.dbURI = metadata
        except:
            self.userdata = metadata


class Subquestion(Question):
    """Subquestion"""
    def get_query(self):
        subqueries = []
        counter = 0

        for subquestion in self.subquestions:
            subquery = self._get_subquery(subquestion, counter, self.rules)
            subqueries.append(subquery)

        query = self._merge_subqueries(subqueries)

        return '?output', query, None

    def _merge_subqueries(self, subqueries):
        pass
