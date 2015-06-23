from refo import Plus
from quepy.parsing import Lemma, Pos, QuestionTemplate, Particle

from dsl import *

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

class Actor(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + LabelOf(name)


class ActedOnQuestion(QuestionTemplate):
    """
    Ex: "Movies starring Winona Ryder"
    """

    keyword = 'starring'

    regex = Lemma("star") + Actor()

    def interpret(self, match):
        movie = HasActor(match.actor) + IsMovie()
        return movie, "enum"


class Subject(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsSubject() + LabelOf(name)


class SubjectQuestion(QuestionTemplate):
    """
    Ex: "Movies about Giant Monsters"
    """

    keyword = 'about'

    regex = Lemma("about") + Subject()

    def interpret(self, match):
        movie = HasSubject(match.subject) + IsMovie()
        return movie, "enum"


class SequelQuestion(QuestionTemplate):
    """
    Ex: "sequel of Godgilla and the Sea Monster"
    """

    keyword = 'sequel of a'

    movie = (Lemma("film") | Lemma("movie"))
    regex = Lemma("sequel") + Lemma("of") + Lemma("a") + movie

    def interpret(self, match):
        return SameAs('input_var') + IsSequel('output_var')
