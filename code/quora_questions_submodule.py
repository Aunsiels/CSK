from question_file_submodule import QuestionFileSubmodule


class QuoraQuestionsSubmodule(QuestionFileSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._filename = "data/questions-quora.txt"
        self._name = "Quora Questions"
