import logging

from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.multiple_module_reference import MultipleModuleReference
from quasimodo.data_structures.multiple_submodule_reference import MultipleSubmoduleReference
from quasimodo.data_structures.multiple_pattern import MultiplePattern


class LinearCombinationSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Linear Combination Submodule"

    def process(self, input_interface):
        logging.info("Start linear combining submodule")
        # group the tuples
        d_gf = dict()
        d_gf_sentences = dict()
        d_gf_modules = dict()
        d_gf_submodules = dict()
        d_gf_patterns = dict()
        for g in input_interface.get_generated_facts():
            fact = g.get_fact()
            if fact in d_gf:
                for score, module_source, submodule_source in g.get_score().scores:
                    d_gf[fact] += score
                    d_gf_modules[fact].add_reference(module_source)
                    d_gf_submodules[fact].add_reference(submodule_source)
                d_gf_sentences[fact] += g.get_sentence_source()
                d_gf_patterns[fact].add_pattern(g.get_pattern())
            else:
                d_gf_modules[fact] = MultipleModuleReference(self._module_reference)
                d_gf_submodules[fact] = MultipleSubmoduleReference(self)
                for score, module_source, submodule_source in g.get_score().scores:
                    d_gf[fact] = score
                    d_gf_modules[fact].add_reference(module_source)
                    d_gf_submodules[fact].add_reference(submodule_source)
                d_gf_sentences[fact] = g.get_sentence_source()
                d_gf_patterns[fact] = MultiplePattern(g.get_pattern())
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
                d_gf_sentences[key],
                d_gf_patterns[key]))
        new_generated_facts = sorted(new_generated_facts,
                                     key=lambda x: -x.get_score())
        return input_interface.replace_generated_facts(new_generated_facts)
