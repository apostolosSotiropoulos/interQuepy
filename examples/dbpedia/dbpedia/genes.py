"""
Questions associated with genes
"""

from refo import Question
from quepy.parsing import Lemma, Pos, QuestionTemplate, Particle
from dsl import AssociatedGene, HasDesease

class Disease(Particle):
    regex = Question(Pos("JJ")) + (Pos("NN") | Pos("NNP") | Pos("NNS")) |\
            Pos("VBN")

    def interpret(self, match):
        return HasDesease(match.words.tokens)

class WhatGenesAssociated(QuestionTemplate):
    """
    Regex for questions like
        "What genes are associated with Acheiropody",
        "What gene is connected to Acheiropody"
    """

    regex = Lemma("what") + Lemma("gene") + Lemma("be") + \
            (Lemma("connect") | Lemma("associate")) + \
            (Lemma("to") | Lemma("with")) + \
            Question(Pos("DT")) + Disease() + Question(Pos("."))

    def interpret(self, match):
        label = AssociatedGene(match.disease)

        return label, "define"