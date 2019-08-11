"""
This is a skeleton for building your own solver.

You just need to find and fix the two TODOs in this file.
"""
from typing import List
import re

import math
import nltk
import spacy

from wordfreq import word_frequency

from aristomini.common.solver import SolverBase
from aristomini.common.models import MultipleChoiceQuestion, MultipleChoiceAnswer, ChoiceConfidence

from quasimodo.spacy_accessor import SpacyAccessor

nlp = spacy.load('en_core_web_sm', disable=["tagger", "parser", "ner"])

class BasicCSKSolver(SolverBase):

    def __init__(self):
        self.name = "Basic CSK Solver"
        self.subject_to_objects = None
        self.object_to_subjects = None
        self.spacy_accessor = SpacyAccessor()

    def solver_info(self) -> str:
        return self.name

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
        choice_texts = [x.text for x in choices]

        question_text = " ".join(self.spacy_accessor.lemmatize(question_text))

        confidences = self.compute_confidences_method1(question_text, choice_texts)

        return MultipleChoiceAnswer(
            [ChoiceConfidence(choice, confidence)
             for choice, confidence in zip(choices, confidences)]
        )

    def compute_confidences_method2(self, question_text, choices):
        confidences: List[float] = []
        associations_question = self.get_subject_associated_words(question_text)
        for choice in choices:
            choice_text = " ".join(self.spacy_accessor.lemmatize(choice))
            associations_choice = self.get_subject_associated_words(choice_text)
            confidences.append(self.compare_two_associations(associations_question, associations_choice))
        return confidences

    def compute_confidences_method1(self, question_text, choices):
        confidences: List[float] = []
        # This frequency helps us to know what are the distinctive elements
        w_freq = self.get_frequency_sequences_in_choices(choices)
        for choice in choices:
            confidence = self.compute_confident_choice_method1(question_text, choice, w_freq)
            confidences.append(confidence)
        return confidences

    def compute_confident_choice_method1(self, question_text, choice, w_freq):
        choice_text = " ".join(self.spacy_accessor.lemmatize(choice))
        propositions = choice_text.lower().split(" ")
        propositions_sub_parts = []
        for i in range(len(propositions)):
            for j in range(i + 1, len(propositions) + 1):
                propositions_sub_parts.append(" ".join(propositions[i:j]))
        confidence = 0
        for subpart in propositions_sub_parts:
            if len(subpart) <= 3:
                continue
            association_score_pairs = self.subject_to_objects.get(subpart, []).copy()
            association_score_pairs += self.object_to_subjects.get(subpart, [])
            confidence_temp = self.get_confidence_associations_for_text(association_score_pairs, question_text)
            confidence_temp /= w_freq.get(subpart, 1.0)
            confidence += confidence_temp
        return confidence

    def get_subject_associated_words(self, sentence):
        association_score_pairs = dict()
        maxi = 0.01
        n_subjects = 0
        for subject in self.subject_to_objects:
            if subject in sentence:
                n_subjects += 1
                for association, score in self.subject_to_objects[subject]:
                    association_score_pairs[association] = association_score_pairs.get(association, 0.0) + math.exp(score)
                    maxi = max(maxi, association_score_pairs[association])
        for obj in self.object_to_subjects:
            if obj in sentence:
                n_subjects += 1
                for association, score in self.object_to_subjects[obj]:
                    association_score_pairs[association] = association_score_pairs.get(association, 0.0) + math.exp(score)
                    maxi = max(maxi, association_score_pairs[association])
        if n_subjects != 0:
            for association in association_score_pairs:
                association_score_pairs[association] /= n_subjects
        tokens = nltk.word_tokenize(sentence)
        for i in range(len(tokens)):
            for j in range(i + 1, len(tokens) + 1):
                word = " ".join(tokens[i:j])
                association_score_pairs[word] = association_score_pairs.get(word, 0.0) + 10.0 * maxi
        return association_score_pairs

    def compare_two_associations(self, association_score_pairs0, association_score_pairs1):
        score = 0
        keys0 = set(association_score_pairs0.keys())
        keys1 = set(association_score_pairs1.keys())
        final_keys = keys0.intersection(keys1)
        for key in final_keys:
            score0 = association_score_pairs0[key]
            score1 = association_score_pairs1[key]
            score += score0 * score1 * key.count(" ")
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
            propositions = self.spacy_accessor.lemmatize(choice.lower())
            for i in range(len(propositions)):
                for j in range(i + 1, len(propositions) + 1):
                    sub_part_choice = " ".join(propositions[i:j])
                    w_freq[sub_part_choice] = w_freq.setdefault(sub_part_choice, 0) + 1
        return w_freq
