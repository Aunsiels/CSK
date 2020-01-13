from quasimodo.serializable import Serializable
from quasimodo.spacy_accessor import get_default_annotator
from .generated_fact_interface import GeneratedFactInterface
from .multiple_source_occurrence import MultipleSourceOccurrence
from .subject import Subject
from .object import Object
from .predicate import Predicate
from .modality import Modality
from .fact import Fact
from nltk.corpus import wordnet as wn


class GeneratedFact(GeneratedFactInterface, Serializable):
    """GeneratedFact
    The default implementation of GeneratedFactInterface
    """

    def to_dict(self):
        res = dict()
        res["type"] = "GeneratedFact"
        res["subject"] = self._subject.to_dict()
        res["predicate"] = self._predicate.to_dict()
        res["object"] = self._object.to_dict()
        if self._modality is not None:
            res["modality"] = self._modality.to_dict()
        else:
            res["modality"] = {"type": "NO_MODALITY"}
        res["negative"] = self._negative
        res["score"] = self._score.to_dict()
        res["sentence_source"] = self._sentence_source.to_dict()
        if self._pattern is not None:
            res["pattern"] = self._pattern.to_dict()
        else:
            res["pattern"] = {"type": "NO_PATTERN"}
        return res

    def __init__(self, subject, predicate, obj, modality, negative, score, sentence_source, pattern=None):
        super().__init__()
        if type(subject) == str:
            self._subject = Subject(subject)
        else:
            self._subject = subject  # SubjectInterface
        if type(predicate) == str:
            self._predicate = Predicate(predicate)
        else:
            self._predicate = predicate  # PredicateInterface
        if type(obj) == str:
            self._object = Object(obj)
        else:
            self._object = obj  # ObjectInterface
        if modality is None:
            self._modality = Modality()
        elif type(modality) == str:
            self._modality = Modality(modality)
        else:
            self._modality = modality  # Optional ModalityInterface
        self._negative = negative
        self._score = score
        self._sentence_source = sentence_source
        self._pattern = pattern

    def get_fact(self):
        return Fact(self.get_subject(),
                    self.get_predicate(),
                    self.get_object(),
                    self.get_modality(),
                    self.is_negative())

    def change_subject(self, new_subject):
        return GeneratedFact(new_subject,
                             self.get_predicate(),
                             self.get_object(),
                             self.get_modality(),
                             self.is_negative(),
                             self.get_score(),
                             self.get_sentence_source(),
                             self.get_pattern())

    def change_predicate(self, new_predicate):
        return GeneratedFact(self.get_subject(),
                             new_predicate,
                             self.get_object(),
                             self.get_modality(),
                             self.is_negative(),
                             self.get_score(),
                             self.get_sentence_source(),
                             self.get_pattern())

    def change_object(self, new_object):
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             new_object,
                             self.get_modality(),
                             self.is_negative(),
                             self.get_score(),
                             self.get_sentence_source(),
                             self.get_pattern())

    def change_modality(self, new_modality):
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             self.get_object(),
                             new_modality,
                             self.is_negative(),
                             self.get_score(),
                             self.get_sentence_source(),
                             self.get_pattern())

    def change_negativity(self, is_negative):
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             self.get_object(),
                             self.get_modality(),
                             is_negative,
                             self.get_score(),
                             self.get_sentence_source(),
                             self.get_pattern())

    def change_score(self, new_score):
        """change_score
        Change the score of the generated fact
        :param new_score: the new score to put
        :type new_score: Float
        :return: A generated fact with the new score
        :rtype: GeneratedFactInterface
        """
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             self.get_object(),
                             self.get_modality(),
                             self.is_negative(),
                             new_score,
                             self.get_sentence_source(),
                             self.get_pattern())

    def change_pattern(self, new_pattern):
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             self.get_object(),
                             self.get_modality(),
                             self.is_negative(),
                             self.get_score(),
                             self.get_sentence_source(),
                             new_pattern)

    def change_sentence(self, new_sentence):
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             self.get_object(),
                             self.get_modality(),
                             self.is_negative(),
                             self.get_score(),
                             new_sentence,
                             self.get_pattern())

    def remove_sentence(self):
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             self.get_object(),
                             self.get_modality(),
                             self.is_negative(),
                             self.get_score(),
                             MultipleSourceOccurrence(),
                             self.get_pattern())

    def get_tsv(self):
        return "\t".join((self.get_subject().get(),
                          self.get_predicate().get(),
                          self.get_object().get(),
                          self.get_modality().get() or " ",
                          str(int(self.is_negative())),
                          str(self.get_score().scores[0][0]),
                          str(self.get_sentence_source())))

    def contains_a_verb_in_predicate(self):
        subject = self.get_subject().get()
        predicate = self.get_predicate().get()
        obj = self.get_object().get()
        predicate_parts = predicate.split(" ")
        if not any([can_be_verb(x) for x in predicate_parts]):
            return False
        n_words_subject = subject.count(" ")
        spacy_annotator = get_default_annotator()
        annotations = spacy_annotator.annotate(subject + " " + predicate + " " + obj)
        counter = 0
        contains_verb = False
        for token in annotations:
            if counter < n_words_subject:
                counter += 1
            else:
                if token.text in predicate and token.pos_ == "VERB":
                    contains_verb = True
        return contains_verb


def can_be_verb(word):
    for synset in wn.synsets(word):
        if synset.pos() == "v":
            return True
    return False
