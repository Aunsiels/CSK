from submodule_interface import SubmoduleInterface
import logging


class CleaningPredicateSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Cleaning predicate"

    def process(self, input_interface):
        logging.info("Start cleaning predicates")
        dirty_words = ["so", "also"]
        new_generated_facts = []
        for g in input_interface.get_generated_facts():
            pred = g.get_predicate().get().split(" ")
            new_pred = []
            for p in pred:
                if p not in dirty_words:
                    new_pred.append(p)
            if len(pred) != len(new_pred):
                g = g.change_predicate(" ".join(new_pred).strip())
            new_generated_facts.append(g)
        return input_interface.replace_generated_facts(new_generated_facts)
