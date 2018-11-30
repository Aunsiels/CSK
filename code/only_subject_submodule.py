from submodule_interface import SubmoduleInterface
from subject import Subject
from inputs import Inputs
import inflect
import logging


class OnlySubjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Only Subject"

    def process(self, input_interface):
        logging.info("Start the filtering the given subjects")
        subjects = set()

        plural_engine = inflect.engine()
        for subject in input_interface.get_subjects():
            subjects.add(subject.get())
            subjects.add(plural_engine.plural(subject.get()))
            sing = plural_engine.singular_noun(subject.get())
            if sing:
                subjects.add(sing)

        subjects.discard("it")
        subjects.discard("its")
        subjects.discard("me")

        new_generated_facts = list(filter(
            lambda x: x.get_subject().get() in subjects,
            input_interface.get_generated_facts()))

        return input_interface.replace_generated_facts(new_generated_facts)
