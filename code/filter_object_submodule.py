from submodule_interface import SubmoduleInterface
import logging


class FilterObjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Filter Object"

    def process(self, input_interface):
        logging.info("Start the filtering object")
        dirty_words = ["their"]
        forbidden = ["used", "called", "xbox", "youtube", "xo", "quote",
                     "quotes", "minecraft", "important", "considered", "why"]
        new_generated_facts = []
        for g in input_interface.get_generated_facts():
            if g.get_object().get() in forbidden:
                continue
            obj = g.get_object().get().split(" ")
            new_obj = []
            for p in obj:
                if p not in dirty_words:
                    new_obj.append(p)
            if len(obj) != len(new_obj):
                g = g.change_object(" ".join(new_obj).strip())
            new_generated_facts.append(g)
        return input_interface.replace_generated_facts(new_generated_facts)
