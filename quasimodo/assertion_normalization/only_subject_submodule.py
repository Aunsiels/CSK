import os
from collections import Counter

from quasimodo.data_structures.submodule_interface import SubmoduleInterface
import logging

from quasimodo.inflect_accessor import DEFAULT_INFLECT

FORGOTTEN_SUBJECTS_FILE = os.path.dirname(
    os.path.realpath(__file__)) + "/../temp/forgotten_subjects.tsv"


def get_subjects_in_all_forms(input_interface):
    subjects = set()
    variations = dict()
    for subject in input_interface.get_subjects():
        original_subject = subject.get().lower()
        variations[original_subject] = original_subject
        subjects.add(original_subject)
        plural_subject = DEFAULT_INFLECT.to_plural(original_subject)
        subjects.add(plural_subject)
        variations[plural_subject] = original_subject
        singular_subject = DEFAULT_INFLECT.to_singular(original_subject)
        if singular_subject:
            subjects.add(singular_subject)
            variations[singular_subject] = original_subject
    subjects.discard("it")
    subjects.discard("its")
    subjects.discard("me")
    return subjects, variations


class OnlySubjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Only Subject"

    def process(self, input_interface):
        logging.info("Start the filtering the given subjects")
        subjects, _ = get_subjects_in_all_forms(input_interface)

        new_generated_facts = list(filter(
            lambda x: x.get_subject().get().lower() in subjects,
            input_interface.get_generated_facts()))

        discarded_generated_facts = list(filter(
            lambda x: x.get_subject().get().lower() not in subjects,
            input_interface.get_generated_facts()))
        forgotten_subjects = [x.get_subject().get()
                              for x in discarded_generated_facts]
        counter_forgotten_subjects = Counter(forgotten_subjects)
        to_save = []
        for subject, value in counter_forgotten_subjects.items():
            to_save.append(subject + "\t" + str(value))
        while True:
            try:
                with open(FORGOTTEN_SUBJECTS_FILE, "w") as f:
                    f.write("\n".join(to_save))
                break
            except OSError as e:
                logging.info("Problem when saving forgotten subjects.  Trying"
                             "again...")
                logging.info(e)
        logging.info("%d facts were removed by the subject cleaner",
                     len(input_interface.get_generated_facts()) - len(
                         new_generated_facts))

        return input_interface.replace_generated_facts(new_generated_facts)
