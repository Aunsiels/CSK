from module_interface import ModuleInterface
from default_submodule_factory import DefaultSubmoduleFactory
from inputs import Inputs

class AssertionGenerationModule(ModuleInterface):
    """AssertionGenerationModule
    A module which generates assertions
    """

    def __init__(self):
        module_names = ["google-autocomplete", "bing-autocomplete"]
        super(AssertionGenerationModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Assertion Generation Module"

    def process(self, input_interface):
        new_inputs = []
        # For now in sequence, we could make it be parallel
        for submodule in self._submodules:
            new_inputs.append(submodule.process(input_interface))
        generated_facts = []
        for inputs in new_inputs:
            generated_facts += inputs.get_generated_facts()
        return input_interface.add_generated_facts(generated_facts)
