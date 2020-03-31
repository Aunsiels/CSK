import logging

from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.inflect_accessor import DEFAULT_INFLECT


class ToSingularSubjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "To Singular Subject Submodule"

    def process(self, input_interface):
        logging.info("Turn subject to singular")
        new_generated_facts = []
        subjects = set([x.get() for x in input_interface.get_subjects()])
        singular_maker = DEFAULT_INFLECT
        for g in input_interface.get_generated_facts():
            subj = g.get_subject().get()
            singular = singular_maker.to_singular(subj)
            if singular not in subjects or singular == subj:
                new_generated_facts.append(g)
            else:
                new_generated_facts.append(g.change_subject(singular))
        return input_interface.replace_generated_facts(new_generated_facts)
