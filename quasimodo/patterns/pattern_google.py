from quasimodo.inflect_accessor import DEFAULT_INFLECT
from quasimodo.serializable import Serializable
from quasimodo.data_structures.pattern_interface import PatternInterface
import re
from nltk.corpus import wordnet


class PatternGoogle(PatternInterface, Serializable):
    """PatternGoogle
    Represents patterns used of autocomplete in search engine
    """

    def to_dict(self):
        res = dict()
        res["type"] = "PatternGoogle"
        res["prefix"] = self._prefix
        res["relation"] = self._relation
        res["negative"] = self._negative
        return res

    def to_str_object(self, obj):
        raise NotImplementedError

    def to_str_so(self, subj, obj):
        raise NotImplementedError

    def __init__(self, prefix, relation="has_property", negative=False):
        super().__init__()
        self._prefix = prefix # we need to give the prefix of the query
        # No score for now
        self._score = 1.0
        self._negative = negative
        self._relation = relation
        self._group = "google-autocomplete"
        self._regex = re.compile(self._prefix.replace("<SUBJ>", ".*")
                                 .replace("<OBJ>", ".*")
                                 .replace("<SUBJS>", ".*"))

    def score_sentence(self, sentence):
        if self.match(sentence):
            return 1.0
        else:
            return 0.0

    def to_str(self):
        return self._prefix

    def to_str_subject(self, subject):
        sing = DEFAULT_INFLECT.to_singular(subject.get())
        plur = DEFAULT_INFLECT.to_plural(subject.get())
        last_sing = ""
        if sing:
            last_sing = sing.split(" ")[-1]
        last_plur = plur.split(" ")[-1]
        if ((not sing or sing == subject.get()) and
                wordnet.synsets(last_plur)) or not wordnet.synsets(last_sing):
            return self._prefix.replace("<SUBJ>", subject.get())\
                .replace("<OBJ>", "")\
                .replace("<SUBJS>", plur)
        else:
            return self._prefix.replace("<SUBJ>", subject.get())\
                .replace("<OBJ>", "")\
                .replace("<SUBJS>", subject.get())

    def match(self, sentence):
        return self._regex.search(sentence) is not None
