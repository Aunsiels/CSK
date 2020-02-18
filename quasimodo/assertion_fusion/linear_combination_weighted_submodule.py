import logging
import os

from quasimodo.parts_of_facts import PartsOfFacts
from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.assertion_fusion.trainer import Trainer
from quasimodo.parameters_reader import ParametersReader


save_weights = True


parameters_reader = ParametersReader()
annotations_file = parameters_reader.get_parameter("annotations-file") or "data/training_active_learning.tsv"
save_file = parameters_reader.get_parameter("weights-file") or os.path.dirname(__file__) + "/../temp/weights.tsv"


def _save_weights(parts_of_facts):
    annotations = get_annotated_data()
    header = parts_of_facts.get_header()
    header.append("label")
    save = ["\t".join(header)]
    for fact in parts_of_facts.get_all_facts():
        row = parts_of_facts.get_fact_row(fact)
        row.append(annotations.get((fact.get_subject().get(),
                                    fact.get_predicate().get(),
                                    fact.get_object().get(),
                                    str(int(fact.is_negative()))),
                                   -1))
        row = [str(x) for x in row]
        save.append("\t".join(row))
    with open(save_file, "w") as f:
        for element in save:
            f.write(element + "\n")


class LinearCombinationWeightedSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Linear Combination Per Module Submodule"

    def process(self, input_interface):
        logging.info("Start linear combining per module submodule")

        logging.info("Grouping facts")
        parts_of_facts = PartsOfFacts.from_generated_facts(input_interface.get_generated_facts())

        if save_weights:
            logging.info("Saving weights facts")
            _save_weights(parts_of_facts)

        logging.info("Training the model...")
        trainer = Trainer(save_file)
        trainer.train()

        logging.info("Generating new facts")
        new_generated_facts = []
        for fact in parts_of_facts.get_all_facts():
            new_generated_facts.append(parts_of_facts.get_generated_fact_with_score_from_classifier(fact, trainer))

        new_generated_facts = sorted(new_generated_facts,
                                     key=lambda x: -sum([score[0] for score in x.get_score().scores]))

        return input_interface.replace_generated_facts(new_generated_facts)


def get_annotated_data():
    annotations = dict()
    with open(annotations_file) as f:
        for line in f:
            line = line.strip().split("\t")
            annotations[(line[0], line[1], line[2], line[3])] = line[4]
    return annotations
