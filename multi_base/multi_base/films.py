from refo import Plus
from quepy.parsing import Lemma, Pos, QuestionTemplate, Particle

from dsl import IsMovie, NameOf, HasActor, IsPerson, LabelOf
from settings import DBP_URI

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))


class Actor(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + LabelOf(name)


class ActedOnQuestion(QuestionTemplate):
    """
    Ex: "List movies with Hugh Laurie"
        "Movies with Matt LeBlanc"
        "In what movies did Jennifer Aniston appear?"
        "Which movies did Mel Gibson starred?"
        "Movies starring Winona Ryder"
    """

    keyword = 'staring'

    acted_on = (Lemma("appear") | Lemma("act") | Lemma("star"))
    movie = (Lemma("movie") | Lemma("movies") | Lemma("film"))
    # regex = (Question(Lemma("list")) + movie + Lemma("with") + Actor()) | \
    #         (Question(Pos("IN")) + (Lemma("what") | Lemma("which")) +
    #          movie + Lemma("do") + Actor() + acted_on + Question(Pos("."))) | \
    #         (Question(Pos("IN")) + Lemma("which") + movie + Lemma("do") +
    #          Actor() + acted_on) | \
    #         (Question(Lemma("list")) + movie + Lemma("star") + Actor())
    regex = Lemma("star") + Actor()

    def interpret(self, match):
        movie = IsMovie() + HasActor(match.actor)
        movie_name = NameOf(movie)
        return movie_name, ("enum", DBP_URI)
