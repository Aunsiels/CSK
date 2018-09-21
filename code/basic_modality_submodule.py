from submodule_interface import SubmoduleInterface
import logging


class BasicModalitySubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Basic modality"

    def process(self, input_interface):
        logging.info("Start basic modality recognition")
        # still has several meanings...
        modality_words = ["always", "commonly", "often", "sometimes",
                          "only", "rarely", "mostly", "especially",
                          "generally", "at_time", "still", "constantly"]
        modality_pred = ["now"]
        new_generated_facts = []
        for g in input_interface.get_generated_facts():
            predicate = g.get_predicate().get().split(" ")
            obj = g.get_object().get().split(" ")
            modality = []
            new_predicate = []
            new_obj = []
            if len(predicate) > 1:
                for pred in predicate:
                    if pred in modality_words or pred in modality_pred:
                        modality.append(pred)
                    else:
                        new_predicate.append(pred)
            else:
                new_predicate = predicate
            if len(obj) > 1:
                for o in obj:
                    if o in modality_words:
                        modality.append(o)
                    else:
                        new_obj.append(o)
            else:
                new_obj = obj
            if len(modality) != 0:
                g = g.change_modality(" ".join(modality).strip())
                if len(predicate) != len(new_predicate):
                    g = g.change_predicate(" ".join(new_predicate).strip())
                if len(obj) != len(new_obj):
                    g = g.change_object(" ".join(new_obj).strip())
            new_generated_facts.append(g)
        return input_interface.replace_generated_facts(new_generated_facts)
