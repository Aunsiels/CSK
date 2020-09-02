from quasimodo.data_structures.modality import get_multiple_parts_combination
from quasimodo.data_structures.submodule_interface import SubmoduleInterface
import logging


class BasicModalitySubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Basic modality"

    def process(self, input_interface):
        logging.info("Start basic modality recognition")
        # still has several meanings...
        modality_words = ["always", "commonly", "often", "sometimes",
                          "only", "rarely", "mostly", "especially",
                          "generally", "at_time", "still", "constantly",
                          "almost", "never"]
        modality_pred = ["now"]
        new_generated_facts = []
        for generated_fact in input_interface.get_generated_facts():
            predicate_split = generated_fact.get_predicate().get().split(" ")
            obj = generated_fact.get_object().get().split(" ")
            modality_d = dict()
            for modality, score in generated_fact.get_modality().get_modalities_and_scores():
                if modality not in modality_d:
                    modality_d[modality] = 0
                modality_d[modality] += score
            new_predicate = []
            new_obj = []
            n_occurrences = generated_fact.get_sentence_source().get_total_number_occurrences()
            if len(predicate_split) > 1:
                for predicate_part in predicate_split:
                    if predicate_part in modality_words or predicate_part in modality_pred:
                        if predicate_part not in modality_d:
                            modality_d[predicate_part] = 0
                        modality_d[predicate_part] += n_occurrences
                    else:
                        new_predicate.append(predicate_part)
            else:
                new_predicate = predicate_split
            if len(obj) > 1:
                for o in obj:
                    if o in modality_words:
                        if o not in modality_d:
                            modality_d[o] = 0
                        modality_d[o] += n_occurrences
                    else:
                        new_obj.append(o)
            else:
                new_obj = obj
            if len(modality_d) != 0:
                generated_fact = generated_fact.change_modality(
                    get_multiple_parts_combination(
                        modality_d.items()
                    ))
                if len(predicate_split) != len(new_predicate):
                    generated_fact = generated_fact.change_predicate(" ".join(new_predicate).strip())
                if len(obj) != len(new_obj):
                    generated_fact = generated_fact.change_object(" ".join(new_obj).strip())
            new_generated_facts.append(generated_fact)
        return input_interface.replace_generated_facts(new_generated_facts)
