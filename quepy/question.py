import logging

from quepy import settings
from quepy import generation
from quepy.tagger import get_tagger, TaggingError
from quepy.encodingpolicy import encoding_flexible_conversion
from quepy.sparql_generation import get_core_sparql_expression

logger = logging.getLogger("quepy.quepyapp")


class Question():
    def __init__(self, subquestions, rules, keywords = None):
        self.subquestions = subquestions
        self.rules = rules
        self.keywords = keywords

    def get_query(self):
        if type(self.subquestions) is list:
            question = Subquestion(self.subquestions, self.rules, self.keywords)
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
        subqueries = self._get_subqueries()

        query = self._merge_subqueries(subqueries)

        return '?output', query, None

    def _get_subqueries(self):
        subqueries = []
        counter = 0
        var_and_type = {}

        for subquestion in self.subquestions:
            rule_matched = self.rules[self.keywords[subquestion[0]]]

            # find default subquery with wrong var names
            question = encoding_flexible_conversion(' '.join(subquestion))
            tagger = get_tagger()
            words = list(tagger(question))
            subquery_expression, meta = rule_matched.get_interpretation(words)
            core_subquery = get_core_sparql_expression(subquery_expression)

            # change variables numbers
            # variables = [w for w in core_subquery.split() if w.startswith('?')]
            # variables = list(set(variables))
            # old_new_vars = [

            # fix input var names
            var_name = self.find_var_name(core_subquery,
                                          rule_matched.metadata['input_type'],
                                          '"input_var"@en')
            if rule_matched.metadata['input_form'] is 'string':
                new_var_name = '?x' + \
                               str(int(var_name.split('x')[1]) + counter * 100)
            else:
                new_var_name = var_and_type[rule_matched.metadata['input_type']]
            core_subquery = core_subquery.replace(var_name, new_var_name)

            # fix output var names
            var_name = self.find_var_name(core_subquery,
                                          rule_matched.metadata['output_type'],
                                          '"ouput_var"@en')
            if rule_matched.metadata['output_type'] in var_and_type:
                new_var_name = var_and_type[rule_matched.metadata['output_type']]
            else:
                new_var_name = var_name
                var_and_type[rule_matched.metadata['output_type']] = var_name
            subquery = core_subquery.replace(var_name, new_var_name)

            db = rule_matched.metadata['db']
            subqueries.append({'db': db, 'query': subquery})

            counter += 1

        final_subquery = 'foo'
        subqueries.append(final_subquery)

        return subqueries

    def _merge_subqueries(self, subqueries):
        grouped_subqueries = {}
        for subquery in subqueries:
            subquery, db = subquery.values()
            if db in grouped_subqueries:
                grouped_subqueries[db] += subquery
            else:
                grouped_subqueries[db] = subquery

        template = u"" + settings.SPARQL_PREAMBLE + "\n" +\
                   u"SELECT DISTINCT ?output WHERE {\n"

        for db, subquery in grouped_subqueries.items():
            template += u"SERVICE <" + db + "> {\n"
            template += u"" + subquery + "}\n"

        template += u"}"

        return template

    def find_var_name(self, query, property, var_name_type):
        for sentence in query.split('.'):
            if var_name_type in sentence:
                return var_name_type
            if property in sentence:
                var_name = [w for w in sentence.split() if w.startswith('?')]
                return var_name[0]
        return 'x0'
