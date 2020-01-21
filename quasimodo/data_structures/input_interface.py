class InputInterface(object):

    def __init__(self):
        self._seeds = [] # List of FactInterface
        self._patterns = [] # List of PatternInterface
        self._generated_facts = [] # List of GeneratedFactInterface
        self._subjects = None
        self._objects = None

    def get_seeds(self):
        """get_seeds
        Gives the seed part of the input
        :return: the seeds
        :rtype: FactInterface
        """
        return self._seeds

    def get_patterns(self, group=None):
        """get_patterns
        Return the pattern part of the input
        :param group: the group of the pattern
        :type group: str
        :return: the seeds
        :rtype: PatternInterface
        """
        if group is None:
            return self._patterns
        else:
            return list(filter(lambda x: x.get_group() == group,
                               self._patterns))

    def get_generated_facts(self):
        """get_generated_facts
        Return the generated facts part of the input
        :return: the generated facts
        :rtype: GeneratedFactInterface
        """
        return self._generated_facts

    def get_subjects(self):
        """get_subjects
        Gives the subjects of the input
        :return: the subjects considered by the input
        :rtype: List[SubjectInterface]
        """
        return self._subjects

    def get_objects(self):
        """get_objects
        Gives the objects of the input
        :return: the objects considered by the input
        :rtype: List[ObjectInterface]
        """
        return self._objects

    def has_subjects(self):
        """has_subjects
        :return: whether the input contains subjects
        :rtype: bool
        """
        return self._subjects is not None

    def has_objects(self):
        """has_objects
        :return: whether the input contains objects
        :rtype: bool
        """
        return self._objects is not None

    def save(self, filename):
        """save
        Saves the object into a file
        :param filename: the file where to save the object
        :type filename: str
        :return: True
        :rtype: bool
        """
        raise NotImplementedError

    def load(self, filename):
        """load
        Loads an input
        :param filename: the file containing the input
        :type filename: str
        :return: a new input
        :rtype: InputInterface
        """
        raise NotImplementedError

    def add_patterns(self, new_patterns):
        """add_patterns
        Adds patterns to the input
        :param new_patterns: the patterns to add
        :type new_patterns: List[PatternInterface]
        :return: a new input
        :rtype: InputInterface
        """
        raise NotImplementedError

    def add_seeds(self, new_seeds):
        """add_seeds
        Adds seeds to the input
        :param new_seeds: the patterns to add
        :type new_seeds: List[FactInterface]
        :return: a new input
        :rtype: InputInterface
        """
        raise NotImplementedError

    def add_generated_facts(self, new_generated_facts):
        """add_generated_facts
        Adds generated facts to the input
        :param new_generated_facts: the generated facts to add
        :type new_generated_facts: List[GeneratedFactInterface]
        :return: a new input
        :rtype: InputInterface
        """
        raise NotImplementedError

    def add_subjects(self, new_subjects):
        """add_subjects
        Adds subjects to the input
        :param new_subjects: the subjects to add
        :type new_subjects: List[SubjectInterface]
        :return: a new input
        :rtype: InputInterface
        """
        raise NotImplementedError

    def add_objects(self, new_objects):
        """add_objects
        Adds objects to the input
        :param new_objects: the objects to add
        :type new_objects: List[ObjectInterface]
        :return: a new input
        :rtype: InputInterface
        """
        raise NotImplementedError

    def replace_patterns(self, new_patterns):
        """replace_patterns
        Replaces patterns to the input
        :param new_patterns: the patterns to replace
        :type new_patterns: List[PatternInterface]
        :return: a new input
        :rtype: InputInterface
        """
        raise NotImplementedError

    def replace_seeds(self, new_seeds):
        """replace_seeds
        Replaces seeds to the input
        :param new_seeds: the patterns to replace
        :type new_seeds: List[FactInterface]
        :return: a new input
        :rtype: InputInterface
        """
        raise NotImplementedError

    def replace_generated_facts(self, new_generated_facts):
        """replace_generated_facts
        Replaces generated facts to the input
        :param new_generated_facts: the generated facts to replace
        :type new_generated_facts: List[GeneratedFactInterface]
        :return: a new input
        :rtype: InputInterface
        """
        raise NotImplementedError

    def replace_subjects(self, new_subjects):
        """replace_subjects
        Replaces subjects to the input
        :param new_subjects: the subjects to replace
        :type new_subjects: List[SubjectInterface]
        :return: a new input
        :rtype: InputInterface
        """
        raise NotImplementedError

    def get_number_subjects(self):
        return len(self._subjects)

    def replace_objects(self, new_objects):
        """replace_objects
        Replaces objects to the input
        :param new_objects: the objects to replace
        :type new_objects: List[ObjectInterface]
        :return: a new input
        :rtype: InputInterface
        """
        raise NotImplementedError
