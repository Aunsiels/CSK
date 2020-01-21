from quasimodo.data_structures.module_interface import ModuleInterface
from quasimodo.default_submodule_factory import DefaultSubmoduleFactory
import logging


class ArchitModule(ModuleInterface):

    def __init__(self):
        module_names = [
            "web-count",
            "web-regression",
            "youtube-count",
            "youtube-regression",
            "flickr-count",
            "flickr-regression",
            "pinterest-count",
            "pinterest-regression",
            "istockphoto-count",
            "istockphoto-regression"
                        ]
        super().__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Archit Module"

    def process(self, input_interface):
        logging.info("Start the archit module")
        for submodule in self._submodules:
            input_interface = submodule.process(input_interface)
        return input_interface
