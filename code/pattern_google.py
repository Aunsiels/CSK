from pattern_interface import PatternInterface

class PatternGoogle(PatternInterface):
    """PatternGoogle
    Represents patterns used of autocomplete in search engine
    """

    def __init__(self,
                 prefix,
                 relation="hasProperty"):
        self._prefix = prefix # we need to give the prefix of the query
        # TODO: have a placeholder for the subject
        # No score for now
        self._score = 1.0
        self._relation = relation
        self._group = "google-autocomplete"

    def score_sentence(self, sentence):
        if self.match(sentence):
            return 1.0
        else:
            return 0.0

    def to_str(self):
        return self._prefix

    def to_str_subject(self, subject):
        # TODO placeholder for subject
        return self._prefix + " " + subject

    def match(self, sentence):
        # TODO improve for placeholder
        return sentence.find(self._prefix) == 0
