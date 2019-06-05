import os


class ParametersReader(object):

    def __init__(self, parameters_file=os.path.dirname(__file__) + "/parameters.tsv"):
        self.parameters = dict()
        with open(parameters_file) as f:
            for line in f:
                line = line.strip().split("\t")
                if len(line) == 2:
                    self.parameters[line[0]] = line[1]

    def get_parameter(self, parameter_name):
        return self.parameters.get(parameter_name, None)