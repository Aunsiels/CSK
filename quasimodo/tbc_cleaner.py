from quasimodo.modality import read_sentence
from .submodule_interface import SubmoduleInterface
import logging


class TBCCleaner(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "TBC Cleaner"

    def process(self, input_interface):
        logging.info("Start the cleaning of TBC")
        new_generated_facts = []
        n_removed = 0
        for generated_fact in input_interface.get_generated_facts():
            modality = generated_fact.get_modality()
            if modality.get_number_completing_parts() == 1:
                n_sentences = generated_fact.get_sentence_source().get_total_number_occurrences()
                n_tbc = 0
                for modality_raw, score in modality.get_modalities_and_scores():
                    if "TBC" in modality_raw:
                        n_tbc = score
                # When we have as many TBC as sentences, it means all contain it and so we can remove the fact
                if n_tbc != n_sentences:
                    new_generated_facts.append(generated_fact)
                else:
                    n_removed += 1
            else:
                new_generated_facts.append(generated_fact)
        logging.info("%d facts were removed by the TBC cleaner", n_removed)
        return input_interface.replace_generated_facts(new_generated_facts)
