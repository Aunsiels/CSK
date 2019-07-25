import os
import logging
import sys

if len(sys.argv) > 1 and ".tsv" in sys.argv[1]:
    DEFAULT_PARAMETERS_FILE = sys.argv[1]
else:
    logging.info("No parameter file given. Use parameters.tsv by default")
    DEFAULT_PARAMETERS_FILE = os.path.dirname(__file__) + "/parameters.tsv"


class ParametersReader(object):

    def __init__(self, parameters_file=DEFAULT_PARAMETERS_FILE):
        self.parameters = dict()
        with open(parameters_file) as f:
            for line in f:
                line = line.strip().split("\t")
                if len(line) == 2:
                    self.parameters[line[0]] = line[1]

    def get_parameter(self, parameter_name):
        return self.parameters.get(parameter_name, None)


parameters_reader = ParametersReader()
