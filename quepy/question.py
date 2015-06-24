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

            subquery = self._get_subquery_by_subquestion_and_rule(\
                                                    subquestion, rule_matched)
            subquery = self._add_offset_to_query_vars(subquery, counter * 10)
            subquery = self._rename_output_var(subquery)
            subquery = self._rename_input_var(subquery, var_and_type, \
                                              rule_matched.input_type)

            out_var = self._find_out_var(subquery, rule_matched.output_type)
            if rule_matched.output_type in var_and_type:
                new_var = var_and_type[rule_matched.output_type]
                subquery = subquery.replace(out_var, new_var)
            else:
                last_output_type = rule_matched.output_type
                last_output_db = rule_matched.db
                var_and_type[last_output_type] = out_var

            subqueries.append({'db': rule_matched.db, 'query': subquery})

            counter += 1

        final_subquery = self._get_final_subquery(last_output_type, \
                                                  var_and_type)
        subqueries.append({'db': last_output_db, 'query': final_subquery})

        return subqueries

    def _get_subquery_by_subquestion_and_rule(self, subquestion, rule):
        question = encoding_flexible_conversion(' '.join(subquestion))
        tagger = get_tagger()
        words = list(tagger(question))
        subquery_expression, meta = rule.get_interpretation(words)
        return get_core_sparql_expression(subquery_expression)

    def _add_offset_to_query_vars(self, query, offset):
        return query.replace(u'?x', u'?x' + str(offset))

    def _rename_output_var(self, query):
        return query.replace('"output_var"@en', '?result')

    def _rename_input_var(self, query, var_and_type, input_type):
        if '"input_var"@en' in query:
            old_var = '"input_var"@en'
            new_var = var_and_type[input_type]
            return query.replace(old_var, new_var)
        return query

    def _find_out_var(self, query, type):
        for sentence in query.split('.'):
            if type in sentence:
                var_name = [w for w in sentence.split() if w.startswith('?')]
                var_name = '?result' if '?result' in query else var_name[0]
                return var_name

    def _get_final_subquery(self, last_output_type, var_and_type):
        input_var = var_and_type[last_output_type]
        return u'\n' + input_var + u' rdfs:label ?output .'

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

