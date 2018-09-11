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

    def get_patterns(self):
        """get_patterns
        Return the pattern part of the input
        :return: the seeds
        :rtype: PatternInterface
        """
        return self._patterns

    def get_generated_facts(self):
        """get_generated_facts
        Return the generated facts part of the input
        :return: the generated facts
        :rtype: GeneratedFactInterface
        """
        return self._generated_facts

    def get_subjects(self):
        return self._subjects

    def get_objects(self):
        return self._objects

    def has_subjects(self):
        return self._subjects is not None

    def has_objects(self):
        return self._objects is not None
