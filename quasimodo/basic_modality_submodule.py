from .submodule_interface import SubmoduleInterface
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
                          "almost"]
        modality_pred = ["now"]
        new_generated_facts = []
        for generated_fact in input_interface.get_generated_facts():
            predicate_split = generated_fact.get_predicate().get().split(" ")
            obj = generated_fact.get_object().get().split(" ")
            modality = []
            new_predicate = []
            new_obj = []
            if len(predicate_split) > 1:
                for predicate_part in predicate_split:
                    if predicate_part in modality_words or predicate_part in modality_pred:
                        modality.append(predicate_part)
                    else:
                        new_predicate.append(predicate_part)
            else:
                new_predicate = predicate_split
            if len(obj) > 1:
                for o in obj:
                    if o in modality_words:
                        modality.append(o)
                    else:
                        new_obj.append(o)
            else:
                new_obj = obj
            if len(modality) != 0:
                generated_fact = generated_fact.change_modality(" ".join(modality).strip())
                if len(predicate_split) != len(new_predicate):
                    generated_fact = generated_fact.change_predicate(" ".join(new_predicate).strip())
                if len(obj) != len(new_obj):
                    generated_fact = generated_fact.change_object(" ".join(new_obj).strip())
            new_generated_facts.append(generated_fact)
        return input_interface.replace_generated_facts(new_generated_facts)
