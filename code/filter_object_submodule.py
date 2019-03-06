from submodule_interface import SubmoduleInterface
import logging


class FilterObjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Filter Object"

    def _is_totally_forbidden(self, sentence, forbidden):
        s = sentence.split(" ")
        for w in s:
            if w in forbidden:
                return True
        return False

    def process(self, input_interface):
        logging.info("Start the filtering object")
        dirty_words = ["their"]
        forbidden = ["used", "called", "xbox", "youtube", "xo", "quote",
                     "quotes", "minecraft", "important", "considered", "why",
                     "using"]
        totally_forbidden = ["xbox", "youtube", "xo", "quote",
                     "quotes", "minecraft", "why", "quizlet", "nz", "wz",
                             "quora", "reddit", "skyrim", "shippuden"]
        new_generated_facts = []
        for g in input_interface.get_generated_facts():
            obj = g.get_object().get()
            if obj in forbidden or \
                    self._is_totally_forbidden(obj, totally_forbidden) or\
                    len(obj) == 1:
                continue
            obj = g.get_object().get().split(" ")
            new_obj = []
            for p in obj:
                if p not in dirty_words:
                    new_obj.append(p)
            if len(obj) != len(new_obj) and len(new_obj) != 0:
                g = g.change_object(" ".join(new_obj).strip())
            if len(new_obj) != 0:
                new_generated_facts.append(g)
        return input_interface.replace_generated_facts(new_generated_facts)
