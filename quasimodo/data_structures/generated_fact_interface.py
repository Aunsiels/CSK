from .fact_interface import FactInterface


class GeneratedFactInterface(FactInterface):
    """GeneratedFactInterface
    Represents a fact which was generated
    """

    def change_subject(self, new_subject):
        raise NotImplementedError

    def change_predicate(self, new_predicate):
        raise NotImplementedError

    def change_object(self, new_object):
        raise NotImplementedError

    def change_modality(self, new_modality):
        raise NotImplementedError

    def change_negativity(self, is_negative):
        raise NotImplementedError

    def __init__(self):
        super().__init__()
        self._score = None
        self._pattern = None # An optional PatternInterface
        self._sentence_source = "" # A string

    def get_score(self):
        """get_score
        Returns the score of the fact
        :return: the score
        :rtype: MultipleScore
        """
        return self._score

    def get_pattern(self):
        """get_pattern
        Returns the pattern from which the fact was extracted, if it exists
        :return: an optional pattern
        :rtype: PatternInterface or None
        """
        return self._pattern

    def get_sentence_source(self):
        """get_sentence_source
        Returns the sentence from which the fact was extracted
        :return: a sentence
        :rtype: str
        """
        return self._sentence_source

    def __str__(self):
        return super().__str__() +\
            " Score: " + str(self.get_score()) +\
            " From pattern: " + str(self.get_pattern()) +\
            " From sentence: " + str(self.get_sentence_source())

    def __repr__(self):
        return str(self)

    def get_fact(self):
        """get_fact
        Get the fact
        :return: The fact
        :rtype: FactInterface
        """
        raise NotImplementedError

    def change_score(self, new_score):
        """change_score
        Change the score of the generated fact
        :param new_score: the new score to put
        :type new_score: Float
        :return: A generated fact with the new score
        :rtype: GeneratedFactInterface
        """
        raise NotImplementedError
