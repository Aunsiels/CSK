from .submodule_interface import SubmoduleInterface
import logging


dirty_words = ["their", "so", "also"]
forbidden = ["used", "called", "xbox", "youtube", "xo", "quote",
             "quotes", "minecraft", "important", "considered", "why",
             "using"]
totally_forbidden = ["xbox", "youtube", "xo", "quote",
                     "quotes", "minecraft", "why", "quizlet", "nz", "wz",
                     "quora", "reddit", "skyrim", "shippuden", "yahoo",
                     "wikipedia", "how", "why", "brainly", "joke", "jokes"]


def _is_totally_forbidden(sentence, forbidden):
    s = sentence.split(" ")
    for w in s:
        if w in forbidden:
            return True
    return False


class FilterObjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Filter Object"

    def process(self, input_interface):
        logging.info("Start the filtering object")
        new_generated_facts = []
        for generated_fact in input_interface.get_generated_facts():
            obj = generated_fact.get_object().get()
            if obj in forbidden or _is_totally_forbidden(obj, totally_forbidden) or len(obj) == 1:
                continue
            obj = generated_fact.get_object().get().split(" ")
            new_obj = []
            for p in obj:
                if p not in dirty_words:
                    new_obj.append(p)
            if len(obj) != len(new_obj) and len(new_obj) != 0:
                generated_fact = generated_fact.change_object(" ".join(new_obj).strip())
            if len(new_obj) != 0:
                new_generated_facts.append(generated_fact)
        return input_interface.replace_generated_facts(new_generated_facts)
