import logging

from quasimodo.parameters_reader import ParametersReader
from quasimodo.data_structures.submodule_interface import SubmoduleInterface
import os.path

parameters_reader = ParametersReader()
filename = parameters_reader.get_parameter("perplexity-file") or \
           os.path.dirname(os.path.realpath(__file__)) + \
           "/../../perplexity/sentences_ppl_sample.tsv"


def _load_perplexity():
    perplexities = dict()
    with open(filename) as f_perplexity:
        for line in f_perplexity:
            p_temp = line.strip().split("\t")
            perplexities[p_temp[0]] = float(p_temp[1])
    return perplexities


def _get_maximum_score(perplexities):
    return max(perplexities.values())


class PerplexitySubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Perplexity submodule"

    def process(self, input_interface):
        logging.info("Start the association submodule for " + self.get_name())
        if filename is None or not os.path.isfile(filename):
            logging.info("No perplexity given")
            return input_interface
        perplexities = _load_perplexity()
        maxi = _get_maximum_score(perplexities)
        for generated_fact in input_interface.get_generated_facts():
            scores = []
            for sentence in generated_fact.get_sentence_source().occurrences:
                if sentence in perplexities:
                    scores.append(perplexities[sentence])
            if scores:
                # Choose a way to aggregate the score as we need a single score
                # Here, minimal perplexity is better
                aggregate = min(scores)
                new_score = aggregate / maxi
                generated_fact.get_score().add_score(new_score,
                                                     self._module_reference,
                                                     self)
        del perplexities
        return input_interface
