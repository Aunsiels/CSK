import logging

from quasimodo.data_structures.object import Object
from quasimodo.data_structures.submodule_interface import SubmoduleInterface

from nltk.stem import WordNetLemmatizer


USELESS_ARTICLE = ["an", "the", "a"]


class SimilarObjectRemover(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Similar Object Remover"

    def process(self, input_interface):
        logging.info("Start the removing of similar objects")
        # Group generated facts by subject, predicate and object
        groups = dict()
        for generated_fact in input_interface.get_generated_facts():
            subject = generated_fact.get_subject()
            if subject not in groups:
                groups[subject] = dict()
            predicate = generated_fact.get_predicate()
            if predicate not in groups[subject]:
                groups[subject][predicate] = set()
            obj = generated_fact.get_object()
            groups[subject][predicate].add(obj)
        lemmatizer = WordNetLemmatizer()
        new_generated_facts = []
        for generated_fact in input_interface.get_generated_facts():
            subject = generated_fact.get_subject()
            predicate = generated_fact.get_predicate()
            obj = generated_fact.get_object().get()
            obj = " ".join([lemmatizer.lemmatize(x) for x in obj.split() if x not in USELESS_ARTICLE])
            obj = Object(obj)
            if obj in groups[subject][predicate]:
                new_generated_facts.append(generated_fact.change_object(obj))
            else:
                new_generated_facts.append(generated_fact)
        return input_interface.replace_generated_facts(new_generated_facts)
