from quasimodo.assertion_normalization.no_personal_submodule import PERSONALS
from quasimodo.assertion_normalization.only_subject_submodule import FORGOTTEN_SUBJECTS_FILE
from quasimodo.assertion_normalization.similar_object_remover import \
    USELESS_ARTICLE
from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.data_structures.subject import Subject
import logging
from os import path
import os

from quasimodo.inflect_accessor import DEFAULT_INFLECT

THRESHOLD_OCCURRENCES = 10

NEW_SUBJECTS_FILE = os.path.dirname(
    os.path.realpath(__file__)) + "/../temp/new_subjects.tsv"


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
        subjects = []
        if path.exists(FORGOTTEN_SUBJECTS_FILE):
            # Read the subjects from a file
            with open(FORGOTTEN_SUBJECTS_FILE, encoding="utf-8") as f:
                for line in f:
                    line = line.strip().split("\t")
                    subject = line[0]
                    if contains_personal(subject) or starts_with_article(subject):
                        continue
                    n_occurrences = int(line[1])
                    if n_occurrences > THRESHOLD_OCCURRENCES:
                        subject_sing = DEFAULT_INFLECT.to_singular(subject)
                        subjects.append(Subject(subject_sing))
        with open(NEW_SUBJECTS_FILE, "a", encoding="utf-8") as f:
            f.write("\n".join([s.get() for s in subjects]) + "\n")
        subjects = []
        if path.exists(NEW_SUBJECTS_FILE):
            with open(NEW_SUBJECTS_FILE, encoding="utf-8") as f:
                for line in f:
                    subject = line.strip()
                    subjects.append(Subject(subject))
        return input_interface.add_subjects(subjects)
