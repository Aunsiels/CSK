from submodule_interface import SubmoduleInterface
from generated_fact import GeneratedFact
import logging


class LinearCombinationSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Linear Combination Submodule"

    def process(self, input_interface):
        logging.info("Start linear combining submodule")
        # group the tuples
        d_gf = dict()
        for g in input_interface.get_generated_facts():
            fact = g.get_fact()
            if fact in d_gf:
                d_gf[fact] += g.get_score()
            else:
                d_gf[fact] = g.get_score()
        # Find the maximum
        maxi = 0.000001
        for key in d_gf:
            maxi = max(maxi, d_gf[key])
        # Normalize
        for key in d_gf:
            d_gf[key] /= maxi
        # Transform to generated facts
        new_generated_facts = []
        for key in d_gf:
            new_generated_facts.append(GeneratedFact(
                key.get_subject(),
                key.get_predicate(),
                key.get_object(),
                key.get_modality(),
                key.is_negative(),
                d_gf[key],
                "",
                self._module_reference,
                self,
                None))
        new_generated_facts = sorted(new_generated_facts,
                                     key=lambda x: -x.get_score())
        return input_interface.replace_generated_facts(new_generated_facts)
