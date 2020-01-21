import os

from quasimodo.assertion_generation.question_file_submodule import QuestionFileSubmodule
from quasimodo.parameters_reader import ParametersReader


parameters_reader = ParametersReader()
FILENAME = parameters_reader.get_parameter("answercom-questions") or \
        os.path.dirname(__file__) + "/data/questions-answerscom-filtered.txt"


class AnswerscomQuestionsSubmodule(QuestionFileSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        # The questions are obtained from the website answers.com
        self._filename = FILENAME
        self._name = "Answers.com Questions"
