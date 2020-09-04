from quasimodo.data_structures.submodule_interface import SubmoduleInterface
import logging


class CleanSubject(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Filter language questions"

    def process(self, input_interface):
        logging.info("Start filtering the language questions")
        new_generated_facts = []
        for g in input_interface.get_generated_facts():
            subject = g.get_subject().get()
            if subject.startswith("a "):
                g = g.change_subject(subject[2:])
            elif subject.startswith("an "):
                g = g.change_subject(subject[2:])
            new_generated_facts.append(g)
        return input_interface.replace_generated_facts(new_generated_facts)
