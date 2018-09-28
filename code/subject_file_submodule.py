from submodule_interface import SubmoduleInterface
from subject import Subject
import logging


class SubjectFileSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Subject File"
        self._filename = ""

    def process(self, input_interface):
        logging.info("Start Subject generation from the file " + self._filename)
        subjects = []
        # Read the subjects from a file
        with open(self._filename) as f:
            for line in f:
                subjects.append(Subject(line.strip()))
        return input_interface.add_subjects(subjects)
