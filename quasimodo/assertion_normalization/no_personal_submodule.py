from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.spacy_accessor import get_default_annotator
import logging

PERSONALS = ["my", "your", "our", "I", "you", "he", "she", "so",
             "such", "me", "this", "that", "here", "there",
             "his", "her", "its"]


def should_be_removed(fact):
    obj_words = fact.get_object().get().split(" ")
    if any([y in PERSONALS for y in obj_words]):
        return True
    if "it" in obj_words:
        spacy_annotator = get_default_annotator()
        spo = fact.get_subject().get() + " " + \
                fact.get_predicate().get() + " " + \
                fact.get_object().get()
        annotation = spacy_annotator.annotate(spo)
        for token in annotation:
            if token.text == "it" and token.dep_ != "nsubj":
                return True
    return False


class NoPersonalSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "No Personal"

    def process(self, input_interface):
        logging.info("Start the removal of personal words")
        new_generated_facts = list(filter(
            lambda x: not should_be_removed(x),
            input_interface.get_generated_facts()))

        logging.info("%d facts were removed by the personal words cleaner",
                     len(input_interface.get_generated_facts()) - len(new_generated_facts))

        return input_interface.replace_generated_facts(new_generated_facts)
