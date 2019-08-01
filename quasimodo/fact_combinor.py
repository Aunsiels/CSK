from quasimodo.parts_of_facts import PartsOfFacts
from .submodule_interface import SubmoduleInterface


class FactCombinor(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Fact Combinor"

    def process(self, input_interface):
        parts_of_facts = PartsOfFacts.from_generated_facts(input_interface.get_generated_facts())
        return input_interface.replace_generated_facts(parts_of_facts.merge_into_generated_facts())
