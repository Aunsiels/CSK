import logging
from submodule_interface import SubmoduleInterface
from generated_fact import GeneratedFact
from multiple_module_reference import MultipleModuleReference
from multiple_submodule_reference import MultipleSubmoduleReference
from multiple_pattern import MultiplePattern


class LinearCombinationWeightedSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Linear Combination Per Module Submodule"
        self._weights = dict()
        # Put weights here
        # Manual for now
        self._weights["Google Autocomplete"] = 10.0
        self._weights["Bing Autocomplete"] = 5.0
        self._weights["Reddit Questions"] = 1.0
        self._weights["Quora Questions"] = 5.0
        self._weights["Antonym Checking"] = 5.0
        self._weights["Simple Wikipedia Cooccurrence"] = 5.0
        self._weights["Wikipedia Cooccurrence"] = 5.0
        self._weights["Answers.com Questions"] = 5.0
        self._total_weights = sum(self._weights.values())

    def process(self, input_interface):
        logging.info("Start linear combining per module submodule")
        # group the tuples
        d_gf = dict()
        d_gf_sentences = dict()
        d_gf_modules = dict()
        d_gf_submodules = dict()
        d_gf_patterns = dict()
        for g in input_interface.get_generated_facts():
            fact = g.get_fact()
            name = g.get_submodule_source().get_name()
            sentence = g.get_sentence_source()
            if fact in d_gf:
                if name in d_gf[fact]:
                    d_gf[fact][name] += g.get_score()
                else:
                    d_gf[fact][name] = g.get_score()
                if sentence in d_gf_sentences[fact]:
                    d_gf_sentences[fact][sentence] += 1
                else:
                    d_gf_sentences[fact][sentence] = 1
                d_gf_modules[fact].add_reference(g.get_module_source())
                d_gf_submodules[fact].add_reference(g.get_submodule_source())
                d_gf_patterns[fact].add_pattern(g.get_pattern())
            else:
                d_gf[fact] = dict()
                d_gf[fact][name] = g.get_score()
                d_gf_sentences[fact] = dict()
                d_gf_sentences[fact][sentence] = 1
                d_gf_modules[fact] = MultipleModuleReference(
                    g.get_module_source())
                d_gf_submodules[fact] = MultipleSubmoduleReference(
                    g.get_submodule_source())
                d_gf_modules[fact].add_reference(self._module_reference)
                d_gf_submodules[fact].add_reference(self)
                d_gf_patterns[fact] = MultiplePattern(g.get_pattern())
        # Compute the new sentences
        for fact in d_gf_sentences:
            d_gf_sentences[fact] = " // ".join([x[0] + " x" + str(x[1])
                                        for x in d_gf_sentences[fact].items()])
        # Get the max of each name for normalization
        d_max = dict()
        for fact in d_gf:
            for name in d_gf[fact]:
                if name in d_max:
                    d_max[name] = max(d_gf[fact][name], d_max[name])
                else:
                    d_max[name] = d_gf[fact][name]
        # Compute the scores
        for fact in d_gf:
            temp = 0
            for name in d_gf[fact]:
                temp += self._weights.setdefault(name, 0.0) * d_gf[fact][name]\
                    / d_max[name]
            d_gf[fact] = temp / self._total_weights
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
                d_gf_modules[key],
                d_gf_submodules[key],
                d_gf_patterns[key]))
        new_generated_facts = sorted(new_generated_facts,
                                     key=lambda x: -x.get_score())
        return input_interface.replace_generated_facts(new_generated_facts)
