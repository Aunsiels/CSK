import logging
import math
from submodule_interface import SubmoduleInterface
from generated_fact import GeneratedFact
from multiple_module_reference import MultipleModuleReference
from multiple_submodule_reference import MultipleSubmoduleReference
from multiple_pattern import MultiplePattern


save_weights = False
save_file = "temp/weights.tsv"

class LinearCombinationWeightedSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Linear Combination Per Module Submodule"
        self._weights = dict()
        # Put weights here
        # Manual for now
        self._weights["Google Autocomplete"] = 0.683
        self._weights["Bing Autocomplete"] = 0.0
        self._weights["Reddit Questions"] = 0.856
        self._weights["Quora Questions"] = 0.924
        self._weights["Antonym Checking"] = 0.0
        self._weights["Simple Wikipedia Cooccurrence"] = 1.51
        self._weights["Wikipedia Cooccurrence"] = 0.914
        self._weights["Image Tag submodule"] = 1.61
        self._weights["Answers.com Questions"] = 0.864
        self._weights["Flickr"] = 1.42
        self._weights["Google Book Submodule"] = 0.0
        self._total_weights = sum([abs(x) for x in self._weights.values()])
        self._intercept = 6.74

    def _save_weights(self, d_gf, d_max):
        save = []
        temp = []
        names = self._weights.keys()
        temp.append("subject")
        temp.append("predicate")
        temp.append("object")
        temp.append("modality")
        temp.append("is negative")
        for name in names:
            temp.append(name)
        save.append("\t".join(temp))
        for fact in d_gf:
            temp = []
            temp.append(fact.get_subject().get())
            temp.append(fact.get_predicate().get())
            temp.append(fact.get_object().get())
            if fact.has_modality():
                temp.append(fact.get_modality().get())
            else:
                temp.append(" ")
            if fact.is_negative():
                temp.append("1")
            else:
                temp.append("0")
            for name in names:
                if name in d_gf[fact]:
                    temp.append(str(d_gf[fact][name] /
                                    d_max.setdefault(name, 1.0)))
                else:
                    temp.append(str(d_gf[fact].setdefault(name, -1.0)))
            save.append("\t".join(temp))
        with open(save_file, "w") as f:
            f.write("\n".join(save))

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
        if save_weights:
            self._save_weights(d_gf, d_max)
        # Compute the scores
        for fact in d_gf:
            temp = 0
            for name in self._weights:
                if name in d_gf[fact]:
                    temp += self._weights[name] * \
                        d_gf[fact][name]\
                        / d_max.setdefault(name, 1.0)
                else:
                    temp += self._weights[name] * -1.0
            temp += self._intercept
            d_gf[fact] = 1.0 / (1.0 + math.exp(-temp))
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
