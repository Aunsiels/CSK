class PatternInterface(object):

    def __init__(self):
        self._score = 0.0 # a float

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
