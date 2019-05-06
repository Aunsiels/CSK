from input_interface import InputInterface

class Inputs(InputInterface):
    """Inputs
    The default implementation of an InputInterface
    """

    def __init__(self,
                 seeds,
                 patterns,
                 generated_facts,
                 subjects=[],
                 objs=[]):
        self._seeds = seeds
        self._patterns = patterns
        self._generated_facts = generated_facts
        self._subjects = set(subjects)
        self._objects = objs

    def add_patterns(self, new_patterns):
        """add_patterns
        Adds patterns to the input
        :param new_patterns: the patterns to add
        :type new_patterns: List[PatternInterface]
        :return: a new input
        :rtype: InputInterface
        """
        return self.replace_patterns(self.get_patterns() + new_patterns)

    def add_seeds(self, new_seeds):
        """add_seeds
        Adds seeds to the input
        :param new_seeds: the patterns to add
        :type new_seeds: List[FactInterface]
        :return: a new input
        :rtype: InputInterface
        """
        return self.replace_seeds(self.get_seeds() + new_seeds)

    def add_generated_facts(self, new_generated_facts):
        """add_generated_facts
        Adds generated facts to the input
        :param new_generated_facts: the generated facts to add
        :type new_generated_facts: List[GeneratedFactInterface]
        :return: a new input
        :rtype: InputInterface
        """
        return self.replace_generated_facts(self.get_generated_facts() +
                                            new_generated_facts)

    def add_subjects(self, new_subjects):
        """add_subjects
        Adds subjects to the input
        :param new_subjects: the subjects to add
        :type new_subjects: List[SubjectInterface]
        :return: a new input
        :rtype: InputInterface
        """
        return self.replace_subjects(self.get_subjects().union(set(new_subjects)))

    def add_objects(self, new_objects):
        """add_objects
        Adds objects to the input
        :param new_objects: the objects to add
        :type new_objects: List[ObjectInterface]
        :return: a new input
        :rtype: InputInterface
        """
        return self.replace_objects(self.get_objects() + new_objects)

    def replace_seeds(self, new_seeds):
        """replace_seeds
        Replaces seeds to the input
        :param new_seeds: the patterns to replace
        :type new_seeds: List[FactInterface]
        :return: a new input
        :rtype: InputInterface
        """
        return Inputs(new_seeds,
                      self.get_patterns(),
                      self.get_generated_facts(),
                      self.get_subjects(),
                      self.get_objects())

    def replace_patterns(self, new_patterns):
        """replace_patterns
        Replaces patterns to the input
        :param new_patterns: the patterns to replace
        :type new_patterns: List[PatternInterface]
        :return: a new input
        :rtype: InputInterface
        """
        return Inputs(self.get_seeds(),
                      new_patterns,
                      self.get_generated_facts(),
                      self.get_subjects(),
                      self.get_objects())

    def replace_generated_facts(self, new_generated_facts):
        """replace_generated_facts
        Replaces generated facts to the input
        :param new_generated_facts: the generated facts to replace
        :type new_generated_facts: List[GeneratedFactInterface]
        :return: a new input
        :rtype: InputInterface
        """
        return Inputs(self.get_seeds(),
                      self.get_patterns(),
                      new_generated_facts,
                      self.get_subjects(),
                      self.get_objects())

    def replace_subjects(self, new_subjects):
        """replace_subjects
        Replaces subjects to the input
        :param new_subjects: the subjects to replace
        :type new_subjects: List[SubjectInterface]
        :return: a new input
        :rtype: InputInterface
        """
        return Inputs(self.get_seeds(),
                      self.get_patterns(),
                      self.get_generated_facts(),
                      set(new_subjects),
                      self.get_objects())

    def replace_objects(self, new_objects):
        """replace_objects
        Replaces objects to the input
        :param new_objects: the objects to replace
        :type new_objects: List[ObjectInterface]
        :return: a new input
        :rtype: InputInterface
        """
        return Inputs(self.get_seeds(),
                      self.get_patterns(),
                      self.get_generated_facts(),
                      self.get_subjects(),
                      new_objects)
