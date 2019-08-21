import os
import re
from collections import Counter
import numpy as np

from quasimodo.parameters_reader import ParametersReader
from .submodule_interface import SubmoduleInterface
import logging

parameters_reader = ParametersReader()
OUT_DIR = parameters_reader.get_parameter("out-dir") or os.path.dirname(__file__) + "/out/"
ANIMALS_FILENAME = parameters_reader.get_parameter("animals50") or os.path.dirname(__file__) + "/data/animals_50.txt"
OCCUPATIONS_FILENAME = parameters_reader.get_parameter("occupations50") or \
                       os.path.dirname(__file__) + "/data/occupations_50.txt"


def get_version():
    version = 1
    regex_output = re.compile(r"quasimodo(?P<version>\d+).tsv")
    for file in os.listdir(OUT_DIR):
        match = regex_output.match(file)
        if match is not None:
            version = max(version, int(match.group("version")))
    return version


class StatisticsSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Statistics Output"

    def process(self, input_interface):
        logging.info("Start statistics output submodule")

        statistics = []

        statistics.append("%d facts generated" % len(input_interface.get_generated_facts()))

        subjects = []
        predicates = []
        objects = []
        for generated_fact in input_interface.get_generated_facts():
            subjects.append(generated_fact.get_subject().get())
            predicates.append(generated_fact.get_predicate().get())
            objects.append((generated_fact.get_object().get()))

        statistics.append("There are %d subjects" % len(set(subjects)))
        statistics.append("There are %d predicates" % len(set(predicates)))
        statistics.append("There are %d objects" % len(set(objects)))

        predicate_counter = Counter(predicates)
        predicates_10 = []
        for key, value in predicate_counter.items():
            if value >= 10:
                predicates_10.append(key)
        statistics.append("%d predicates appear more than 10 times" % len(predicates_10))

        statistics.append("There are %0.2f facts per subject" %
                          (len(input_interface.get_generated_facts()) / len(set(subjects))))

        animals = []
        with open(ANIMALS_FILENAME) as f:
            for line in f:
                animals.append(line.strip())
        animal_facts = 0
        animals_found = set()
        for subject in subjects:
            if subject in animals:
                animal_facts += 1
                animals_found.add(subject)
        print("There are %d facts about animals" % animal_facts)
        print("%d different animals were found", len(animals_found))

        occupations = []
        with open(OCCUPATIONS_FILENAME) as f:
            for line in f:
                occupations.append(line.strip())
        occupations_facts = 0
        occupations_found = set()
        for subject in subjects:
            if subject in occupations:
                occupations_facts += 1
                occupations_found.add(subject)
        print("There are %d facts about occupations" % occupations_facts)
        print("%d different occupations were found", len(occupations_found))

        n_found = dict()
        interesting_submodules = [
            "Google Autocomplete",
            "Answers.com Questions",
            "Reddit Questions",
            "Yahoo Questions",
            "Quora Questions",
            "Bing Autocomplete",
            "CoreNLP",
            "OpenIE5",
            "Manual"
        ]
        scores = []
        for generated_fact in input_interface.get_generated_facts():
            scores_temp = generated_fact.get_score().scores
            submodules_temp = set()
            for score, _, submodule_source in scores_temp:
                submodules_temp.add(submodule_source.get_name())
                scores.append(score)
            for submodule in interesting_submodules:
                if submodule in submodules_temp:
                    n_found[submodule] = n_found.get(submodule, 0) + 1

        for submodule in interesting_submodules:
            statistics.append("%.2f facts were extracted from %s" %
                              ((n_found.get(submodule, 0) / len(input_interface.get_generated_facts()) * 100),
                                submodule))

        statistics.append("The mean score is %.2f and the standard deviation is %.2f" %
                          (float(np.mean(scores)), float(np.std(scores))))

        while True:
            version = get_version()
            with open(OUT_DIR + "statistics" + str(version) + ".txt") as f:
                f.write("\n".join(statistics))
                break

        return input_interface
