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
            if g.get_module_source().get_name() == self._module_reference.get_name():
                continue
            subj = g.get_subject().get()
            obj = g.get_object().get()
            pred = g.get_predicate().get()
            if g.is_negative():
                pred = "not " + pred
            for synset in wn.synsets(obj):
                for lemma in synset.lemmas():
                    for antonym in lemma.antonyms():
                        if subj in antonyms:
                            if pred in antonyms[subj]:
                                antonyms[subj][pred].add(antonym)
                            else:
                                antonyms[subj][pred] = {antonym}
                        else:
                            antonyms[subj] = dict()
                            antonyms[subj][pred] = {antonym}
        new_generated_facts = []
        for g in input_interface.get_generated_facts():
            if g.get_module_source().get_name() == self._module_reference.get_name():
                continue
            found = False
            subj = g.get_subject().get()
            obj = g.get_object().get()
            pred = g.get_predicate().get()
            if g.is_negative():
                pred = "not " + pred
            for synset in wn.synsets(obj):
                if found:
                    break
                for lemma in synset.lemmas():
                    if lemma in antonyms.setdefault(subj, dict())\
                            .setdefault(pred, []):
                        found = True
                        break
            if not found:
                new_generated_facts.append(
                    g.change_score(1.0)
                    .change_module_source(self._module_reference)
                    .change_submodule_source(self)
                    .remove_sentence())
        return input_interface.add_generated_facts(new_generated_facts)
