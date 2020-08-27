from quasimodo.data_structures.submodule_interface import SubmoduleInterface
import logging


dirty_words = ["their", "so", "also"]
forbidden = ["used", "called", "xbox", "youtube", "xo", "quote",
             "quotes", "minecraft", "important", "considered", "why",
             "using", "as", "for", "as a", "like", "doing", "the", "would",
             "of", "in", "now", "tonight", "today"]
totally_forbidden = ["xbox", "youtube", "xo", "quote",
                     "quotes", "minecraft", "why", "quizlet", "nz", "wz",
                     "quora", "reddit", "skyrim", "shippuden", "yahoo",
                     "wikipedia", "how", "why", "brainly", "joke", "jokes", "quiz"]


def _is_totally_forbidden(sentence, forbidden):
    s = sentence.split(" ")
    if "quiz let" in sentence:
        return True
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
            predicate = generated_fact.get_predicate().get()
            if predicate == obj[0]:
                obj = obj[1:]
            # Remove last punctuation
            changed_last = False
            if obj and obj[-1] and not obj[-1][-1].isalnum():
                obj[-1] = obj[-1][:-1]
                changed_last = True
            new_obj = []
            for p in obj:
                if p not in dirty_words:
                    new_obj.append(p)
            if (obj != new_obj or changed_last) and len(new_obj) != 0:
                generated_fact = generated_fact.change_object(" ".join(new_obj).strip())
            if len(new_obj) != 0:
                new_generated_facts.append(generated_fact)

        logging.info("%d facts were removed by the object cleaner",
                     len(input_interface.get_generated_facts()) - len(new_generated_facts))

        return input_interface.replace_generated_facts(new_generated_facts)
