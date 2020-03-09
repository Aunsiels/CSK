from quasimodo.assertion_normalization.no_personal_submodule import PERSONALS
from quasimodo.assertion_normalization.only_subject_submodule import FORGOTTEN_SUBJECTS_FILE
from quasimodo.assertion_normalization.similar_object_remover import \
    USELESS_ARTICLE
from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.data_structures.subject import Subject
import logging
from os import path

THRESHOLD_OCCURRENCES = 10


def contains_personal(subject):
    subject_split = subject.split(" ")
    return any([word in PERSONALS for word in subject_split])


def starts_with_article(subject):
    subject_split = subject.split(" ")
    if len(subject_split) > 0 and subject_split[0] in USELESS_ARTICLE:
        return True
    return False


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
                if contains_personal(subject) or starts_with_article(subject):
                    continue
                n_occurrences = int(line[1])
                if n_occurrences > THRESHOLD_OCCURRENCES:
                    subjects.append(Subject(subject))
        return input_interface.add_subjects(subjects)
