import json

from quasimodo import serialized_object_reader
from .input_interface import InputInterface

OBJECTS = "objects"

SUBJECTS = "subjects"

GENERATED_FACTS = "generated_facts"

PATTERNS = "patterns"

SEEDS = "seeds"


class Inputs(InputInterface):
    """Inputs
    The default implementation of an InputInterface
    """

    def __init__(self, seeds=None, patterns=None, generated_facts=None, subjects=None, objs=None):
        super().__init__()
        self._seeds = seeds or []
        self._patterns = patterns or []
        self._generated_facts = generated_facts or []
        self._subjects = subjects or set()
        self._objects = objs or []

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

    def save(self, filename):
        """save
        Saves the object into a file
        :param filename: the file where to save the object
        :type filename: str
        :return: True
        :rtype: bool
        """
        dump = dict()
        dump[SEEDS] = [x.to_dict() for x in self._seeds]
        dump[PATTERNS] = [x.to_dict() for x in self._patterns]
        dump[GENERATED_FACTS] = [x.to_dict() for x in self._generated_facts]
        dump[SUBJECTS] = [x.to_dict() for x in self._subjects]
        dump[OBJECTS] = [x.to_dict() for x in self._objects]
        with open(filename, "w") as f:
            json.dump(dump, f)
        return True

    def load(self, filename):
        """load
        Loads an input
        :param filename: the file containing the input
        :type filename: str
        :return: a new input
        :rtype: InputInterface
        """
        read_input = Inputs()
        with open(filename, "r") as f:
            input_json = json.load(f)
            read_input = read_input.replace_seeds(serialized_object_reader.read_seeds(input_json[SEEDS]))
            read_input = read_input.replace_patterns(serialized_object_reader.read_patterns(input_json[PATTERNS]))
            read_input = read_input.replace_generated_facts(
                serialized_object_reader.read_generated_facts(input_json[GENERATED_FACTS]))
            read_input = read_input.replace_subjects(serialized_object_reader.read_subjects(input_json[SUBJECTS]))
            read_input = read_input.replace_objects(serialized_object_reader.read_objects(input_json[OBJECTS]))
        return read_input
