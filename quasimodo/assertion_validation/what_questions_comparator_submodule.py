from quasimodo.parameters_reader import ParametersReader
from quasimodo.assertion_validation.sentence_comparator import SentenceComparator

parameters_reader = ParametersReader()
WHAT_QUESTION_FILE = parameters_reader.get_parameter("what-questions-file") or ""


class WhatQuestionsComparatorSubmodule(SentenceComparator):

    def __init__(self, module_reference):
        super().__init__(module_reference, WHAT_QUESTION_FILE)
        self._name = "What questions file"
