"""
This is a skeleton for building your own solver.

You just need to find and fix the two TODOs in this file.
"""
from typing import List
import re

import nltk
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
            res.append(x.lemma_)
            #if x.pos_ == "VERB":
            #    res.append(x.lemma_)
            #else:
            #    res.append(x.text)
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

        question_text = question.stem.lower()
        choices = question.choices

        question_text = self.lemmatize(question_text)

        confidences: List[float] = []

        # This frequency helps us to know what are the distinctive elements
        w_freq = self.get_frequency_sequences_in_choices(choices)

        for i, choice in enumerate(question.choices):
            label = choice.label
            choice_text = self.lemmatize(choice.text)

            propositions = choice_text.lower().split(" ")
            propositions_subparts = []
            for i in range(len(propositions)):
                for j in range(i + 1, len(propositions) + 1):
                    propositions_subparts.append(" ".join(propositions[i:j]))

            confidence = 0

            for subpart in propositions_subparts:
                if len(subpart) <= 3:
                    continue
                association_score_pairs = self.subject_to_objects.get(subpart, [])
                association_score_pairs += self.object_to_subjects.get(subpart, [])
                confidence_temp = self.get_confidence_associations_for_text(association_score_pairs, question_text)
                confidence_temp /= w_freq[subpart]
                confidence += confidence_temp
            confidences.append(confidence)


        return MultipleChoiceAnswer(
            [ChoiceConfidence(choice, confidence)
             for choice, confidence in zip(choices, confidences)]
        )

    def get_subject_associated_words(self, sentence):
        association_score_pairs = dict()
        for word in nltk.word_tokenize(sentence):
            association_score_pairs[word] = association_score_pairs.get(word, 0.0) + 1.0
        for subject in self.subject_to_objects:
            if subject in sentence:
                for association, score in self.subject_to_objects[subject]:
                    association_score_pairs[association] = association_score_pairs.get(association, 0.0) + score
        return association_score_pairs

    def compare_two_associations(self, association_score_pairs0, association_score_pairs1):
        score = 0
        keys0 = set(association_score_pairs0.keys())
        keys1 = set(association_score_pairs1.keys())
        final_keys = keys0.intersection(keys1)
        for key in final_keys:
            score += association_score_pairs0[key] * association_score_pairs1[key]
        return score

    def get_confidence_associations_for_text(self, association_score_pairs, question_text):
        confidence_temp = 0
        done = set()
        for (association, score) in association_score_pairs:
            if re.search("[^0-9a-zA-Z]" + re.escape(association) +
                         "[^0-9a-zA-Z]", question_text) is not None \
                    and association not in done:
                done.add(association)
                confidence_temp += score * 1.0 / self.get_frequency(association)
        return confidence_temp

    def get_frequency_sequences_in_choices(self, choices):
        w_freq = dict()
        for i, choice in enumerate(choices):
            propositions = self.lemmatize(choice.text.lower()).split(" ")
            for i in range(len(propositions)):
                for j in range(i + 1, len(propositions) + 1):
                    sub_part_choice = " ".join(propositions[i:j])
                    w_freq[sub_part_choice] = w_freq.setdefault(sub_part_choice, 0) + 1
        return w_freq
