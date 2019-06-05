from .pattern_interface import PatternInterface


class MultiplePattern(PatternInterface):

    def __init__(self, pattern=None):
        super().__init__()
        if pattern is not None and not isinstance(pattern, MultiplePattern):
            self._patterns = [pattern]
            self._score = pattern.get_score()
            self._relation = pattern.get_relation()
            self._group = pattern.get_group()
            self._negative = pattern.is_negative()
        else:
            self._patterns = []
            self._score = 0
            self._relation = ""
            self._group = ""
            self._negative = False
        if isinstance(pattern, MultiplePattern):
            for pattern_temp in pattern._patterns:
                self.add_pattern(pattern_temp)

    def add_pattern(self, pattern):
        if isinstance(pattern, MultiplePattern):
            for pattern_temp in pattern._patterns:
                self.add_pattern(pattern_temp)
        elif pattern is not None:
            self._patterns.append(pattern)
            self._score = sum([pattern.get_score()
                               for pattern in self._patterns]) / \
                len(self._patterns)
            self._relation = "; ".join(set([pattern.get_relation()
                                            for pattern in self._patterns]))
            self._group = "; ".join(set([pattern.get_group()
                                         for pattern in self._patterns]))
            # TODO: something more clever?
            self._negative = all([pattern.is_negative()
                                  for pattern in self._patterns])

    def match(self, sentence):
        """match
        Whether a sentence match the current pattern
        :param sentence: The sentence to check
        :type sentence: str
        :return: whether the sentence matches or not
        :rtype: Boolean
        """
        return all([pattern.match(sentence) for pattern in self._patterns])

    def score_sentence(self, sentence):
        """score_sentence
        Gives a score to a sentence
        :param sentence: a sentence to score
        :type sentence: str
        :return: the score of the sentence
        :rtype: float
        """
        return sum([pattern.score_sentence(sentence)
                    for pattern in self._patterns]) / len(self._patterns)

    def to_str(self):
        """to_str
        Gets a string representation of the pattern
        :return: a string representing the pattern
        :rtype: str
        """
        return "; ".join(set([pattern.to_str() for pattern in self._patterns]))

    def to_str_subject(self, subject):
        """to_str_subject
        Returns the pattern with the subject
        :param subject: the subject to add to the pattern
        :type subject: str
        :return: The pattern with the subject in it
        :rtype: str
        """
        return "; ".join([pattern.to_str_subject(subject)
                          for pattern in self._patterns])

    def to_str_object(self, obj):
        """to_str_object
        Gives the patterns with a fix object
        :param obj: the object to include
        :type obj: str
        :return: the pattern with the obj fixed
        :rtype: str
        """
        return "; ".join([pattern.to_str_object(obj)
                          for pattern in self._patterns])

    def to_str_so(self, subj, obj):
        """to_str_so
        Gives the pattern with both the subject and the object fixed
        :param subj: The subject to fix
        :type subj: str
        :param obj: The object to fix
        :type obj: str
        :return: the pattern completly fixed
        :rtype: str
        """
        return "; ".join([pattern.to_str_so(subj, obj)
                          for pattern in self._patterns])
