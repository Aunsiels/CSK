from fact_interface import FactInterface

class GeneratedFactInterface(FactInterface):
    """GeneratedFactInterface
    Represents a fact which was generated
    """

    def __init__(self):
        self._score = 0.0 # a float
        self._pattern = None # An optional PatternInterface
        self._sentence_source = "" # A string
        self._module_source = None # A ModuleReferenceInterface
        self._submodule_source = None # A SubmoduleReferenceInterface

    def get_score(self):
        """get_score
        Returns the score of the fact
        :return: the score
        :rtype: Flaot
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

    def get_module_source(self):
        """get_module_source
        Returns the module which extracted the fact
        :return: a module reference
        :rtype: ModuleReferenceInterface
        """
        return self._module_source

    def get_submodule_source(self):
        """get_submodule_source
        Returns the submodule which extracted the fact
        :return: a submodule reference
        :rtype: SubmoduleReferenceInterface
        """
        return self._submodule_source

    def __str__(self):
        return super().__str__() +\
            " Score: " + str(self.get_score()) +\
            " From pattern: " + str(self.get_pattern()) +\
            " From module: " + str(self.get_module_source().get_name()) +\
            " From submodule: " + str(self.get_submodule_source().get_name()) +\
            " From sentence: " + str(self.get_sentence_source())
