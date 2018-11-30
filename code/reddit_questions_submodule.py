from question_file_submodule import QuestionFileSubmodule


class RedditQuestionsSubmodule(QuestionFileSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        # Reddit questions are obtained from a dump of Reddit
        self._filename = "data/why-how-questions-filtered.txt"
        self._name = "Reddit Questions"
