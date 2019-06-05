import logging
import os

from .multiple_scores import MultipleScore
from .submodule_interface import SubmoduleInterface
from .generated_fact import GeneratedFact
from .multiple_module_reference import MultipleModuleReference
from .multiple_submodule_reference import MultipleSubmoduleReference
from .multiple_pattern import MultiplePattern
from .trainer import Trainer


save_weights = True
save_file = os.path.dirname(__file__) + "/temp/weights.tsv"
annotations_file = os.path.dirname(__file__) + "/temp/all_manual_annotations.tsv"


def read_sentence(sentence):
    res = []
    sentence_parts = sentence.split(" // ")
    for part in sentence_parts:
        part_score = part.split("x#x")
        if len(part_score) == 1:
            res.append((part_score[0].strip(), 1))
        else:
            res.append((part_score[0].strip(), int(part_score[1])))
    return res


class LinearCombinationWeightedSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Linear Combination Per Module Submodule"
        self._weights = set()

    def _get_fact_row(self, fact, d_gf, d_max, d_gf_modality, d_gf_patterns, d_gf_sentences):
        names = self._weights
        temp = [fact.get_subject().get(), fact.get_predicate().get(), fact.get_object().get()]
        modality = d_gf_modality[fact]
        if modality:
            temp.append(modality)
        else:
            temp.append(" ")
        if fact.is_negative():
            temp.append(1)
        else:
            temp.append(0)
        temp.append(d_gf_patterns[fact].to_str())
        for name in names:
            if name in d_max and d_max[name] == 0:
                d_max[name] = 1
            if name in d_gf[fact]:
                if name in d_max:
                    temp.append(d_gf[fact][name] /
                                d_max[name])
                else:
                    temp.append(d_gf[fact][name])
            else:
                temp.append("")
        temp.append(sum(d_gf_sentences[fact].values()))
        return temp

    def _save_weights(self, d_gf, d_max, d_gf_modality, d_gf_patterns, d_gf_sentences):
        save = []
        temp = []
        annotations = get_annotated_data()
        names = self._weights
        temp.append("subject")
        temp.append("predicate")
        temp.append("object")
        temp.append("modality")
        temp.append("is negative")
        temp.append("patterns")
        for name in names:
            temp.append(name)
        temp.append("number sentences")
        temp.append("label")
        save.append("\t".join(temp))
        for fact in d_gf:
            row = self._get_fact_row(fact, d_gf, d_max, d_gf_modality, d_gf_patterns, d_gf_sentences)
            row.append(annotations.get((fact.get_subject().get(),
                                        fact.get_predicate().get(),
                                        fact.get_object().get()),
                                       -1))
            row = [str(x) for x in row]
            save.append("\t".join(row))
        with open(save_file, "w") as f:
            for element in save:
                f.write(element + "\n")

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
        logging.info("Grouping facts")
        for generated_fact in input_interface.get_generated_facts():
            fact = generated_fact.get_fact()
            modality = fact.get_modality()
            if modality is not None:
                modality = modality.get()
            else:
                modality = ""
            fact = fact.change_modality("")
            sentence_source = generated_fact.get_sentence_source()
            for _, module_source, submodule_source in generated_fact.get_score().scores:
                self._weights.add(submodule_source.get_name())
            if len(modality) ==  0 or "TBC" not in modality:
                df_valid.add(fact)
            if fact in d_gf:
                for score, module_source, submodule_source in generated_fact.get_score().scores:
                    if submodule_source.get_name() in d_gf[fact]:
                        d_gf[fact][submodule_source.get_name()] += score
                    else:
                        d_gf[fact][submodule_source.get_name()] = score
                    d_gf_modules[fact].add_reference(module_source)
                    d_gf_submodules[fact].add_reference(submodule_source)
                if len(sentence_source) > 0:
                    for sentence, score in read_sentence(sentence_source):
                        d_gf_sentences[fact][sentence] = d_gf_sentences[fact].get(sentence, 0) + score
                if len(modality) > 0:
                    for modality_temp, score in read_sentence(modality):
                        d_gf_modality[fact][modality_temp] = d_gf_modality[fact].get(modality_temp, 0) + score
                d_gf_patterns[fact].add_pattern(generated_fact.get_pattern())
            else:
                d_gf[fact] = dict()
                d_gf_modules[fact] = MultipleModuleReference(self._module_reference)
                d_gf_submodules[fact] = MultipleSubmoduleReference(self)
                for score, module_source, submodule_source in generated_fact.get_score().scores:
                    d_gf[fact][submodule_source.get_name()] = score
                    d_gf_modules[fact].add_reference(module_source)
                    d_gf_submodules[fact].add_reference(submodule_source)
                d_gf_sentences[fact] = dict()
                d_gf_patterns[fact] = MultiplePattern(generated_fact.get_pattern())
                d_gf_modality[fact] = dict()
                if len(sentence_source) > 0:
                    for sentence, score in read_sentence(sentence_source):
                        d_gf_sentences[fact][sentence] = d_gf_sentences[fact].get(sentence, 0) + score
                if len(modality) > 0:
                    for modality_temp, score in read_sentence(modality):
                        d_gf_modality[fact][modality_temp] = d_gf_modality[fact].get(modality_temp, 0) + score
        # Remove completely incomplete facts
        to_delete = []
        logging.info("Deleting " + str(len(to_delete)) + " TBC facts")
        for fact in to_delete:
            del d_gf[fact]
            del d_gf_sentences[fact]
            del d_gf_modules[fact]
            del d_gf_submodules[fact]
            del d_gf_patterns[fact]
            del d_gf_modality[fact]
        logging.info("Computing new sentences")

        # Compute the new modalities
        logging.info("Computing new modalities")
        for fact in d_gf_modality:
            number_tbc = 0
            total = 0
            for modality in d_gf_modality[fact]:
                total += d_gf_modality[fact][modality]
                if "TBC" in modality:
                    number_tbc += d_gf_modality[fact][modality]
            d_gf[fact]["TBC"] = 0.0
            if total > 0:
                if total == number_tbc:
                    d_gf[fact]["TBC"] = 1.0
            d_gf_modality[fact] = " // ".join([x[0] + " x#x" + str(x[1])
                                               for x in d_gf_modality[fact].items()
                                               if x[0] != ""])
        # Get the max of each name for normalization
        logging.info("Computing max")
        d_max = dict()
        for fact in d_gf:
            for name in d_gf[fact]:
                if name in d_max:
                    d_max[name] = max(d_gf[fact][name], d_max[name])
                else:
                    d_max[name] = d_gf[fact][name]
        if save_weights:
            self._save_weights(d_gf, d_max, d_gf_modality, d_gf_patterns, d_gf_sentences)

        # Compute the scores
        logging.info("Scoring the facts...")
        d_scores = dict()
        trainer = Trainer(save_file)
        trainer.train()
        for fact in d_gf:
            row = self._get_fact_row(fact, d_gf, d_max, d_gf_modality, d_gf_patterns, d_gf_sentences)
            d_scores[fact] = trainer.predict(fact, row)

        # Compute the new sentences
        for fact in d_gf_sentences:
            d_gf_sentences[fact] = " // ".join([x[0] + " x#x" + str(x[1])
                                        for x in d_gf_sentences[fact].items()])

        # Transform to generated facts
        new_generated_facts = []
        for key in d_gf:
            multiple_score = MultipleScore()
            multiple_score.add_score(d_scores[key], d_gf_modules[key], d_gf_submodules[key])
            new_generated_facts.append(GeneratedFact(
                key.get_subject(),
                key.get_predicate(),
                key.get_object(),
                d_gf_modality[key],
                key.is_negative(),
                multiple_score,
                d_gf_sentences[key],
                d_gf_patterns[key]))
        new_generated_facts = sorted(new_generated_facts,
                                     key=lambda x: -sum([score[0] for score in x.get_score().scores]))
        return input_interface.replace_generated_facts(new_generated_facts)


def get_annotated_data():
    annotations = dict()
    with open(annotations_file) as f:
        for line in f:
            line = line.strip().split("\t")
            annotations[(line[0], line[1], line[2])] = line[3]
    return annotations
