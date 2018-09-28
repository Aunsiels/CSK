from submodule_interface import SubmoduleInterface
from nltk.corpus import wordnet as wn
import logging


class AntonymCheckingSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Antonym Checking"

    def process(self, input_interface):
        logging.info("Start the antonym checking")
        antonyms = dict()
        for g in input_interface.get_generated_facts():
            for synset in wn.synsets(g.get_object().get()):
                for lemma in synset.lemmas():
                    for antonym in lemma.antonyms():
                        if g.get_subject().get() in antonyms:
                            antonyms[g.get_subject().get()].add(antonym)
                        else:
                            antonyms[g.get_subject().get()] = {antonym}
        new_generated_facts = []
        for g in input_interface.get_generated_facts():
            found = False
            for synset in wn.synsets(g.get_object().get()):
                if found:
                    break
                for lemma in synset.lemmas():
                    if lemma in antonyms.setdefault(g.get_subject().get(), []):
                        found = True
                        break
            if not found:
                new_generated_facts.append(
                    g.change_score(1.0)
                    .change_module_source(self._module_reference)
                    .change_submodule_source(self))
            else:
                new_generated_facts.append(
                    g.change_score(0.0)
                    .change_module_source(self._module_reference)
                    .change_submodule_source(self))
        return input_interface.add_generated_facts(new_generated_facts)
