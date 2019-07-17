"""
This is a skeleton for building your own solver.

You just need to find and fix the two TODOs in this file.
"""
from typing import List
import re
import spacy

from wordfreq import word_frequency

from aristomini.common.solver import SolverBase
from aristomini.common.models import MultipleChoiceQuestion, MultipleChoiceAnswer, ChoiceConfidence

nlp = spacy.load('en_core_web_sm', disable=["tagger", "parser", "ner"])

class BasicCSKSolver(SolverBase):

    def __init__(self):
        self.name = "Basic CSK Solver"
        self.subject_to_objects = None
        self.object_to_subjects = None

    def solver_info(self) -> str:
        return self.name

    def lemmatize(self, s):
        doc = nlp(s)
        res = []
        for x in doc:
            if x.pos_ == "VERB":
                res.append(x.lemma_)
            else:
                res.append(x.text)
        return " ".join(res)

    def get_frequency(self, sentence):
        words = sentence.split(" ")
        freq = 1.0
        for word in words:
            freq *= word_frequency(word, "en")
        if freq == 0:
            freq = 1
        return freq

    def answer_question(self, question: MultipleChoiceQuestion) -> MultipleChoiceAnswer:
        # pylint: disable=unused-variable

        stem = question.stem.lower()
        choices = question.choices

        stem = self.lemmatize(stem)

        confidences: List[float] = []

        w_freq = dict()
        for i, choice in enumerate(choices):
            propositions = self.lemmatize(choice.text.lower()).split(" ")
            for i in range(len(propositions)):
                for j in range(i + 1, len(propositions) + 1):
                    word = " ".join(propositions[i:j])
                    w_freq[word] = w_freq.setdefault(word, 0) + 1

        for i, choice in enumerate(question.choices):
            label = choice.label
            text = self.lemmatize(choice.text)

            propositions = text.lower().split(" ")
            propositions_c = []
            for i in range(len(propositions)):
                for j in range(i + 1, len(propositions) + 1):
                    propositions_c.append(" ".join(propositions[i:j]))

            # TODO: compute confidence
            confidence = 0

            for prop in propositions_c:
                done = set()
                if len(prop) <= 3:
                    continue
                if prop in self.subject_to_objects:
                    for (asso, score) in self.subject_to_objects[prop]:
                        if re.search("[^0-9a-zA-Z]" + re.escape(asso) +
                                     "[^0-9a-zA-Z]", stem) is not None\
                                and asso not in done:
                            done.add(asso)
                            confidence += score * 1 / self.get_frequency(asso) \
                                / w_freq[prop]
                if prop in self.object_to_subjects:
                    for (asso, score) in self.object_to_subjects[prop]:
                        if re.search("[^0-9a-zA-Z]" + re.escape(asso) +
                                     "[^0-9a-zA-Z]", stem) is not None\
                                and asso not in done:
                            done.add(asso)
                            confidence += score * 1 / self.get_frequency(asso) \
                                / w_freq[prop]

            confidences.append(confidence)


        return MultipleChoiceAnswer(
            [ChoiceConfidence(choice, confidence)
             for choice, confidence in zip(choices, confidences)]
        )
