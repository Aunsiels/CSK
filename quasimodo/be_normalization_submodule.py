from .submodule_interface import SubmoduleInterface
import logging


def starts_by_word(sentence, word):
    return sentence.startswith(word + " ") or sentence == word


def replace_first_word(sentence, replacement):
    sentence = sentence.split(" ")
    sentence[0] = replacement
    sentence = " ".join(sentence)
    return sentence


def process_generated_fact(generated_fact):
    predicate = generated_fact.get_predicate().get()
    if starts_by_word(predicate, "is") or starts_by_word(predicate, "are"):
        predicate = replace_first_word(predicate, "be")
        new_generated_fact = generated_fact.change_predicate(predicate)
    elif starts_by_word(predicate, "were"):
        predicate = replace_first_word(predicate, "was")
        new_generated_fact = generated_fact.change_predicate(predicate)
    else:
        new_generated_fact = generated_fact
    return new_generated_fact


class BeNormalizationSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Be Normalization"

    def process(self, input_interface):
        logging.info("normalize the form of be")
        new_gfs = []
        for gf in input_interface.get_generated_facts():
            new_generated_fact = process_generated_fact(gf)
            new_gfs.append(new_generated_fact)
        return input_interface.replace_generated_facts(new_gfs)
