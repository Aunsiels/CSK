import logging
import string

import nltk

from quasimodo.data_structures.submodule_interface import SubmoduleInterface


class UselessPunctuationCleaner(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Useless Punctuation Cleaner"

    def process(self, input_interface):
        logging.info("Start the removal of the punctuation")
        new_generated_facts = []
        for generated_fact in input_interface.get_generated_facts():
            obj = generated_fact.get_object().get()
            tokens = nltk.word_tokenize(obj)
            while tokens and tokens[-1] in string.punctuation:
                tokens = tokens[:-1]
            if tokens:
                new_generated_fact = generated_fact.change_object(" ".join(tokens))
                new_generated_facts.append(new_generated_fact)
        return input_interface.replace_generated_facts(new_generated_facts)