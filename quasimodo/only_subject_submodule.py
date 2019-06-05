from .submodule_interface import SubmoduleInterface
import inflect
import logging


class OnlySubjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Only Subject"

    def process(self, input_interface):
        logging.info("Start the filtering the given subjects")
        subjects = set()

        plural_engine = inflect.engine()
        for subject in input_interface.get_subjects():
            subjects.add(subject.get().lower())
            subjects.add(plural_engine.plural(subject.get().lower()))
            sing = plural_engine.singular_noun(subject.get().lower())
            if sing:
                subjects.add(sing)

        subjects.discard("it")
        subjects.discard("its")
        subjects.discard("me")

        new_generated_facts = list(filter(
            lambda x: x.get_subject().get().lower() in subjects,
            input_interface.get_generated_facts()))

        return input_interface.replace_generated_facts(new_generated_facts)
