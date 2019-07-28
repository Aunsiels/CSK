from .submodule_interface import SubmoduleInterface
import inflect
import logging


def get_subjects_in_all_forms(input_interface):
    subjects = set()
    variations = dict()
    plural_engine = inflect.engine()
    for subject in input_interface.get_subjects():
        original_subject = subject.get().lower()
        variations[original_subject] = original_subject
        subjects.add(original_subject)
        plural_subject = plural_engine.plural(original_subject)
        subjects.add(plural_subject)
        variations[plural_subject] = original_subject
        singular_subject = plural_engine.singular_noun(original_subject)
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

        logging.info("%d facts were removed by the subject cleaner",
                     len(input_interface.get_generated_facts()) - len(new_generated_facts))

        return input_interface.replace_generated_facts(new_generated_facts)
