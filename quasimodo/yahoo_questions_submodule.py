import os

from quasimodo.question_file_submodule import QuestionFileSubmodule
from quasimodo.parameters_reader import ParametersReader


parameters_reader = ParametersReader()
FILENAME = parameters_reader.get_parameter("yahoo-questions") or \
        os.path.dirname(__file__) + "/data/questions-yahoo.txt"


class YahooQuestionsSubmodule(QuestionFileSubmodule):
    """ Yahoo Questions are obtained by downloading them from \
        https://webscope.sandbox.yahoo.com/. More precisely:
        * L5 - Yahoo! Answers Manner Questions, version 2.0
        * L6 - Yahoo! Answers Comprehensive Questions and Answers version 1.0

        Then, we run:
            grep "<subject>" FullOct2007.xml | sed -i "s/<subject>//g" | \
                sed -i "s/<\/subject>//g" | \
                grep -i "^\(why\|how\) \(do\|does\|can\|cannot\|are\|is\)" > questions.txt
    """

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._filename = FILENAME
        self._name = "Yahoo Questions"
