from submodule_interface import SubmoduleInterface
import logging
import inflect

p = inflect.engine()

class ToSingularSubjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "To Singular Subject Submodule"

    def process(self, input_interface):
        logging.info("Turn subject to singular")
        new_generated_facts = []
        for g in input_interface.get_generated_facts():
            sing = p.singular_noun(g.get_subject().get())
            if not sing:
                new_generated_facts.append(g)
            else:
                new_generated_facts.append(g.change_subject(sing))
        return input_interface.replace_generated_facts(new_generated_facts)
