class FactInterface(object):
    """FactInterface
    Represents a fact
    """

    def __init__(self):
        self._subject = None # SubjectInterface
        self._predicate = None # PredicateInterface
        self._object = None # ObjectInterface
        self._modality = None # Optinal ModalityInterface
        self._negative = False

    def get_subject(self):
        """get_subject
        The subject of the fact
        :return: The subject
        :rtype: SubjectInterface
        """
        return self._subject

    def get_predicate(self):
        """get_predicate
        Gives the predicate of the fact
        :return: the predicate
        :rtype: PredicateInterface
        """
        return self._predicate

    def get_object(self):
        """get_object
        Gives the object of the fact
        :return: the object
        :rtype: ObjectInterface
        """
        return self._object

    def get_modality(self):
        """get_modality
        Gives the modality of the fact
        :return: the optional modality
        :rtype: ModalityInterface or None
        """
        return self._modality

    def has_modality(self):
        """has_modality
        Whether the fact has a modality
        :return: has the fact a modality
        :rtype: Boolean
        """
        return self._modality is not None

    def is_negative(self):
        """is_negative
        :return: whether the fact is negative or not
        :rtype: bool
        """
        return self._negative

    def __str__(self):
        return "(" + str(self.get_subject()) + ", " + \
            str(self.get_predicate()) + ", " + \
            str(self.get_object()) + ")"
