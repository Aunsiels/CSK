from submodule_interface import SubmoduleInterface
import logging
import inflect

p = inflect.engine()
non_plural = ["texas", "star wars", "gas", "people"]

class ToSingularSubjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "To Singular Subject Submodule"

    def process(self, input_interface):
        logging.info("Turn subject to singular")
        new_generated_facts = []
        for g in input_interface.get_generated_facts():
            subj = g.get_subject().get()
            sing = p.singular_noun(subj)
            if not sing or subj in non_plural or subj.endswith("sis"):
                new_generated_facts.append(g)
            else:
                new_generated_facts.append(g.change_subject(sing))
        return input_interface.replace_generated_facts(new_generated_facts)
