import os

from quasimodo.assertion_generation.question_file_submodule import QuestionFileSubmodule
from quasimodo.parameters_reader import ParametersReader


parameters_reader = ParametersReader()
FILENAME = parameters_reader.get_parameter("quora-questions") or \
        os.path.dirname(__file__) + "/data/questions-quora.txt"


class QuoraQuestionsSubmodule(QuestionFileSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._filename = FILENAME
        self._name = "Quora Questions"
