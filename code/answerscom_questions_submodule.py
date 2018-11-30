from question_file_submodule import QuestionFileSubmodule


class AnswerscomQuestionsSubmodule(QuestionFileSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        # The questions are obtained from the website answers.com
        self._filename = "data/questions-answerscom-filtered.txt"
        self._name = "Answers.com Questions"
