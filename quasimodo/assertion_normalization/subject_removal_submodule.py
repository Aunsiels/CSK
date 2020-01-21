from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.data_structures.subject import Subject
import logging


to_remove = ["it", "some", "one", "we", "a", "b", "c",
        "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w",
        "x", "y", "z", "you", "he", "she", "they", "me",
        "an", "someone", "mr", "ms", "anyone", "1", "2",
        "3", "4", "5", "6", "7", "8", "9"]


class SubjectRemovalSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Subject Removal"

    def process(self, input_interface):
        logging.info("Start removing some subjects")
        subjects = set(input_interface.get_subjects())
        for subject in to_remove:
            subject = Subject(subject)
            if subject in subjects:
                subjects.remove(subject)
        subjects = list(subjects)
        return input_interface.replace_subjects(subjects)
