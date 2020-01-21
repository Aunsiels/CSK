class PatternInterface(object):
    """PatternInterface
    Represents a pattern
    """

    def __init__(self):
        self._score = 0.0 # a float
        self._relation = None
        self._group = ""
        self._negative = False

    def match(self, sentence):
        """match
        Whether a sentence match the current pattern
        :param sentence: The sentence to check
        :type sentence: str
        :return: whether the sentence matches or not
        :rtype: Boolean
        """
        raise NotImplementedError

    def score_sentence(self, sentence):
        """score_sentence
        Gives a score to a sentence
        :param sentence: a sentence to score
        :type sentence: str
        :return: the score of the sentence
        :rtype: float
        """
        raise NotImplementedError

    def to_str(self):
        """to_str
        Gets a string representation of the pattern
        :return: a string representing the pattern
        :rtype: str
        """
        raise NotImplementedError

    def to_str_subject(self, subject):
        """to_str_subject
        Returns the pattern with the subject
        :param subject: the subject to add to the pattern
        :type subject: str
        :return: The pattern with the subject in it
        :rtype: str
        """
        raise NotImplementedError

    def to_str_object(self, obj):
        """to_str_object
        Gives the patterns with a fix object
        :param obj: the object to include
        :type obj: str
        :return: the pattern with the obj fixed
        :rtype: str
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def get_score(self):
        """get_score
        Gives the score of the pattern
        :return: the score
        :rtype: float
        """
        return self._score

    def get_relation(self):
        """get_relation
        Get the relation of the pattern
        :return: the relation
        :rtype: Option[str]
        """
        return self._relation

    def get_group(self):
        """get_group
        Get the group of the pattern
        :return: the group
        :rtype: str
        """
        return self._group

    def __str__(self):
        return "Pattern(" + self.to_str() + ", " +\
            "Relation=" + str(self._relation) + ", " +\
            "Score=" + str(self.get_score()) + ", " +\
            "Group=" + str(self.get_group()) + ")"

    def is_negative(self):
        return self._negative
