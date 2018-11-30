import logging
from submodule_interface import SubmoduleInterface
from fact import Fact

class ConceptNetSeedsSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "ConceptNet Seeds"
        self._filename = "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/"\
            "commonsense_data/ConceptNet/conceptnet_20k.tsv"

    def process(self, input_interface):
        logging.info("Start ConceptNet Seeds gathering")
        facts = []
        with open(self._filename) as f:
            for line in f:
                line = line.strip()
                spo = line.split("\t")
                facts.append(Fact(spo[0], spo[1], spo[2]))
        logging.info("%d seeds from ConceptNet where loaded", len(fact))
        return input_interface.add_seeds(facts)
