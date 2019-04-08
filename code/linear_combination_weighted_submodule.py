import logging
import math
from submodule_interface import SubmoduleInterface
from generated_fact import GeneratedFact
from multiple_module_reference import MultipleModuleReference
from multiple_submodule_reference import MultipleSubmoduleReference
from multiple_pattern import MultiplePattern


save_weights = True
save_file = "temp/weights.tsv"

class LinearCombinationWeightedSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Linear Combination Per Module Submodule"
        self._weights = dict()
        # Put weights here
        self._weights["Google Autocomplete"] = 0.8727
        self._weights["Bing Autocomplete"] = 0.0
        self._weights["Reddit Questions"] = 0.5240
        self._weights["Quora Questions"] = 1.3898
        self._weights["Antonym Checking"] = 0.0
        self._weights["Simple Wikipedia Cooccurrence"] = 0.2660
        self._weights["Wikipedia Cooccurrence"] = 0.2811
        self._weights["Image Tag submodule"] = 0.9172
        self._weights["Answers.com Questions"] = 1.0221
        self._weights["Flickr"] = 0.8527
        self._weights["Google Book Submodule"] = 0.8627
        self._weights["Web count"] = 0.0
        self._weights["Web regression"] = 0.0
        self._weights["Youtube count"] = 0.0
        self._weights["Youtube regression"] = 0.0
        self._weights["Flickr count"] = 0.0
        self._weights["Flickr regression"] = 0.0
        self._weights["Pinterest count"] = 0.0
        self._weights["Pinterest regression"] = 0.0
        self._weights["Istockphoto count"] = 0.0
        self._weights["Istockphoto regression"] = 0.0
        self._weights["TBC"] = -0.3762
        self._total_weights = sum([abs(x) for x in self._weights.values()])
        # self._intercept = 5.7423
        self._intercept = 5.6673

    def _save_weights(self, d_gf, d_max, d_gf_modality, d_gf_patterns):
        save = []
        temp = []
        names = self._weights.keys()
        temp.append("subject")
        temp.append("predicate")
        temp.append("object")
        temp.append("modality")
        temp.append("is negative")
        temp.append("patterns")
        for name in names:
            temp.append(name)
        save.append("\t".join(temp))
        for fact in d_gf:
            temp = []
            temp.append(fact.get_subject().get())
            temp.append(fact.get_predicate().get())
            temp.append(fact.get_object().get())
            modality = d_gf_modality[fact]
            if modality:
                temp.append(modality)
            else:
                temp.append(" ")
            if fact.is_negative():
                temp.append("1")
            else:
                temp.append("0")
            temp.append(d_gf_patterns[fact].to_str())
            for name in names:
                if name in d_gf[fact]:
                    if name in d_max:
                        temp.append(str(d_gf[fact][name] /
                                        d_max[name]))
                    else:
                        temp.append(str(d_gf[fact][name]))
                else:
                    if name in d_gf[fact]:
                        temp.append(str(d_gf[fact][name]))
                    else:
                        temp.append("-1")
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
        d_gf_modality = dict()
        df_valid = set()
        for g in input_interface.get_generated_facts():
            fact = g.get_fact()
            modality = fact.get_modality()
            fact = fact.change_modality("")
            name = g.get_submodule_source().get_name()
            sentence = g.get_sentence_source()
            if g.get_module_source().get_name() == "Assertion Generation Module"\
                    and (modality is None or
                         "TBC" not in modality.get()):
                df_valid.add(fact)
            if fact in d_gf:
                if name in d_gf[fact]:
                    d_gf[fact][name] += g.get_score()
                else:
                    d_gf[fact][name] = g.get_score()
                if sentence in d_gf_sentences[fact]:
                    d_gf_sentences[fact][sentence] += 1
                else:
                    d_gf_sentences[fact][sentence] = 1
                if modality in d_gf_modality[fact]:
                    d_gf_modality[fact][modality] += 1
                else:
                    d_gf_modality[fact][modality] = 1
                if g.get_module_source().get_name() == "Assertion Generation Module"\
                        and (modality is None or
                             "TBC" not in modality.get()):
                    df_valid.add(fact)
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
                d_gf_modality[fact] = dict()
                d_gf_modality[fact][modality] = 1
        # Remove completly incomplete facts
        to_delete = []
        # for fact in d_gf:
        #     if fact not in df_valid:
        #         to_delete.append(fact)
        logging.info("Deleting " + str(len(to_delete)) + " TBC facts")
        for fact in to_delete:
            del d_gf[fact]
            del d_gf_sentences[fact]
            del d_gf_modules[fact]
            del d_gf_submodules[fact]
            del d_gf_patterns[fact]
            del d_gf_modality[fact]
        # Compute the new sentences
        for fact in d_gf_sentences:
            d_gf_sentences[fact] = " // ".join([x[0] + " x" + str(x[1])
                                        for x in d_gf_sentences[fact].items()])
        # Compute the new modalities
        for fact in d_gf_modality:
            number_tbc = 0
            total = 0
            for x in d_gf_modality[fact]:
                total += d_gf_modality[fact][x]
                if x is not None and "TBC" in x.get():
                    number_tbc += d_gf_modality[fact][x]
            d_gf[fact]["TBC"] = 0.0
            if total > 0:
                if total == number_tbc:
                    d_gf[fact]["TBC"] = 1.0
            d_gf_modality[fact] = " // ".join([x[0].get() + " x" + str(x[1])
                                               for x in d_gf_modality[fact].items()
                                               if x[0] is not None and x[0].get() != ""])
        # Get the max of each name for normalization
        d_max = dict()
        for fact in d_gf:
            for name in d_gf[fact]:
                if name in d_max:
                    d_max[name] = max(d_gf[fact][name], d_max[name])
                else:
                    d_max[name] = d_gf[fact][name]
        if save_weights:
            self._save_weights(d_gf, d_max, d_gf_modality, d_gf_patterns)
        d_scores = dict()
        # Compute the scores
        for fact in d_gf:
            temp = 0
            for name in self._weights:
                if name in d_gf[fact]:
                    weight = -1.0
                    if d_gf[fact][name] > 0:
                        weight = d_gf[fact][name]
                    temp += self._weights[name] * \
                        weight\
                        / d_max.setdefault(name, 1.0)
                else:
                    temp += self._weights[name] * -1.0
            temp += self._intercept
            d_scores[fact] = 1.0 / (1.0 + math.exp(-temp))
        # Transform to generated facts
        new_generated_facts = []
        for key in d_gf:
            # if key not in df_valid:
            #     continue
            new_generated_facts.append(GeneratedFact(
                key.get_subject(),
                key.get_predicate(),
                key.get_object(),
                d_gf_modality[key],
                key.is_negative(),
                d_scores[key],
                d_gf_sentences[key],
                d_gf_modules[key],
                d_gf_submodules[key],
                d_gf_patterns[key]))
        new_generated_facts = sorted(new_generated_facts,
                                     key=lambda x: -x.get_score())
        return input_interface.replace_generated_facts(new_generated_facts)
