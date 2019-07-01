import os

from quasimodo.question_file_submodule import QuestionFileSubmodule
from quasimodo.parameters_reader import ParametersReader


parameters_reader = ParametersReader()
FILENAME = parameters_reader.get_parameter("reddit-questions") or \
        os.path.dirname(__file__) + "/data/questions-reddit.txt"



class RedditQuestionsSubmodule(QuestionFileSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        # Reddit questions are obtained from a dump of Reddit
        self._filename = FILENAME
        self._name = "Reddit Questions"
