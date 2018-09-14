from pattern_interface import PatternInterface
import re
import inflect

plural_engine = inflect.engine()

class PatternGoogle(PatternInterface):
    """PatternGoogle
    Represents patterns used of autocomplete in search engine
    """

    def __init__(self,
                 prefix,
                 relation="hasProperty"):
        self._prefix = prefix # we need to give the prefix of the query
        # No score for now
        self._score = 1.0
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
        return self._prefix.replace("<SUBJ>", subject.get())\
            .replace("<OBJ>", "")\
            .replace("<SUBJS>", plural_engine.plural(subject.get()))

    def match(self, sentence):
        return self._regex.search(sentence) is not None
