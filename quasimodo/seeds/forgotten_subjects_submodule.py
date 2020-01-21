from quasimodo.assertion_normalization.only_subject_submodule import FORGOTTEN_SUBJECTS_FILE
from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.data_structures.subject import Subject
import logging
from os import path

THRESHOLD_OCCURRENCES = 10


class ForgottenSubjectsSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Forgotten subjects submodule"

    def process(self, input_interface):
        logging.info("Start getting forgotten subjects")
        if not path.exists(FORGOTTEN_SUBJECTS_FILE):
            return input_interface
        subjects = []
        # Read the subjects from a file
        with open(FORGOTTEN_SUBJECTS_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip().split("\t")
                subject = line[0]
                n_occurrences = int(line[1])
                if n_occurrences > THRESHOLD_OCCURRENCES:
                    subjects.append(Subject(subject))
        return input_interface.add_subjects(subjects)