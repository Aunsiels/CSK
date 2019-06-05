import logging

from .parameters_reader import ParametersReader
from .submodule_interface import SubmoduleInterface
from .fact import Fact

parameters_reader = ParametersReader()
SEEDS_LOCATION = parameters_reader.get_parameter("conceptnet-seeds") or ""


class ConceptNetSeedsSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "ConceptNet Seeds"

    def process(self, input_interface):
        logging.info("Start ConceptNet Seeds gathering")
        facts = []
        with open(SEEDS_LOCATION) as f:
            for line in f:
                line = line.strip()
                spo = line.split("\t")
                facts.append(Fact(spo[0], spo[1], spo[2]))
        logging.info("%d seeds from ConceptNet where loaded", len(facts))
        return input_interface.add_seeds(facts)
