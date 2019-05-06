from submodule_interface import SubmoduleInterface
from nltk.corpus import wordnet as wn
from subject import Subject
import logging


class SubjectsWordnetSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Subject Wordnet"

    def process(self, input_interface):
        logging.info("Start subjects from wordnet")
        subjects = []
        all_lemma_names = [x.lemma_names()
                           for x in wn.all_synsets() if x.pos() == "n"]
        all_lemmas = set()
        for lemma_names in all_lemma_names:
            for lemma_name in lemma_names:
                all_lemmas.add(lemma_name.replace("_", " ").lower())
        for subject in all_lemmas:
            subjects.append(Subject(subject))
        return input_interface.add_subjects(subjects)
