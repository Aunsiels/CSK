from module_interface import ModuleInterface
from default_submodule_factory import DefaultSubmoduleFactory
import logging

class AllSeedsModule(ModuleInterface):

    def __init__(self):
        module_names = ["animal-seeds", "occupations-seeds",
                        "conceptnet-subjects"]
        super(AllSeedsModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "All Seeds module"

    def process(self, input_interface):
        logging.info("Generate all seeds")
        for sm in self._submodules:
            input_interface = sm.process(input_interface)
        return input_interface
