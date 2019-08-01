from .submodule_interface import SubmoduleInterface
import logging
import inflect

p = inflect.engine()
non_plural = ["texas", "star wars", "gas", "people", "chaos", "fetus", "moses",
              "jesus", "gps", "abs"]


class ToSingularSubjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "To Singular Subject Submodule"

    def process(self, input_interface):
        logging.info("Turn subject to singular")
        new_generated_facts = []
        subjects = set([x.get() for x in input_interface.get_subjects()])
        conversion = dict()
        for g in input_interface.get_generated_facts():
            subj = g.get_subject().get()
            if subj in conversion:
                sing = conversion[subj]
            else:
                sing = p.singular_noun(subj)
                conversion[subj] = sing
            if not sing or subj in non_plural or subj.endswith("sis") or\
                    sing not in subjects:
                new_generated_facts.append(g)
            else:
                new_generated_facts.append(g.change_subject(sing))
        return input_interface.replace_generated_facts(new_generated_facts)
