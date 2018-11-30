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
        negation = ""
        if self.is_negative():
            negation = "not "
        if self.has_modality():
            return negation + "(" + str(self.get_subject()) + ", " + \
                str(self.get_predicate()) + ", " + \
                str(self.get_object()) + ")[" + str(self.get_modality()) + "]"
        return negation + "(" + str(self.get_subject()) + ", " + \
            str(self.get_predicate()) + ", " + \
            str(self.get_object()) + ")"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.get_subject()) +\
            hash(self.get_modality()) +\
            hash(self.get_object()) +\
            hash(self.get_predicate()) +\
            hash(self.is_negative())

    def __eq__(self, other):
        if not isinstance(other, FactInterface):
            return False
        return self.get_subject() == other.get_subject() and\
            self.get_predicate() == other.get_predicate() and\
            self.get_object() == other.get_object() and\
            self.get_modality() == other.get_modality() and\
            self.is_negative() == other.is_negative()

    def change_subject(self, new_subject):
        """change_subject
        Return a new fact with the subject changed
        :param new_subject: the new subject to put
        :type new_subject: str or SubjectInterface
        :return: the new fact
        :rtype: FactInterface
        """
        raise NotImplementedError

    def change_predicate(self, new_predicate):
        """change_predicate
        Change the predicate of the fact
        :param new_predicate: the predicate to write
        :type new_predicate: str or PredicateInterface
        :return: a new fact
        :rtype: FactInterface
        """
        raise NotImplementedError

    def change_object(self, new_object):
        """change_object
        Change the object of the fact
        :param new_object: the object to update
        :type new_object: str or ObjectInterface
        :return: a new fact
        :rtype: FactInterface
        """
        raise NotImplementedError

    def change_modality(self, new_modality):
        """change_modality
        Change the modality of the fact
        :param new_modality: the new modality to update
        :type new_modality: str or ModalityInterface
        :return: a new fact
        :rtype: FactInterface
        """
        raise NotImplementedError
