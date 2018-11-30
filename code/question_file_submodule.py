import logging
import inflect
from statement_maker import StatementMaker
from openie_fact_generator_submodule import OpenIEFactGeneratorSubmodule
from pattern_google import PatternGoogle
import re


_plural_engine = inflect.engine()

class QuestionFileSubmodule(OpenIEFactGeneratorSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._name = "Question File Submodule"
        self._filename = None  # To define

    def _read_questions(self):
        questions = []
        with open(self._filename) as f:
            for line in f:
                questions.append(line.strip().lower())
        return questions

    def _to_suggestion(self, question, subjects):
        # No pattern, rank 1 by default
        # We take the subject the closest to the beginning
        # and the longest in case of equality
        min_pos = len(question)
        length = 0
        subject_final = ""
        # Only check the third word for now
        for word in question.split(" ")[2:3]:
            if word in subjects:
                for subject in subjects[word]:
                    temp0 = question.find(subject[0])
                    temp1 = question.find(subject[1])
                    len_temp = len(subject[0])
                    if temp0 != -1 and temp0 < min_pos:
                        min_pos = temp0
                        subject_final = subject[0]
                        length = len_temp
                    elif temp0 != -1 and temp0 == min_pos and len_temp > length:
                        subject_final = subject[0]
                        length = len_temp
                    elif temp1 != -1 and temp1 < min_pos:
                        min_pos = temp1
                        subject_final = subject[0]
                        length = len_temp
                    elif temp1 != -1 and temp1 == min_pos and len_temp > length:
                        subject_final = subject[0]
                        length = len_temp
                if subject_final != "":
                    break
        pattern = None
        if question.startswith("why are ") and \
                not question.startswith("why are not"):
            pattern = PatternGoogle("why are <SUBJS>")
        elif question.startswith("why is ") and \
                not question.startswith("why is not"):
            pattern = PatternGoogle("why is <SUBJ>")
        elif question.startswith("why does ") and \
                not question.startswith("why does not"):
            pattern = PatternGoogle("why does <SUBJ>")
        elif question.startswith("why do ") and \
                not question.startswith("why do not"):
            pattern = PatternGoogle("why do <SUBJS>")
        elif question.startswith("why can "):
            pattern = PatternGoogle("why can <SUBJS>", "CAN")
        elif question.startswith("why can't "):
            pattern = PatternGoogle("why can't <SUBJS>", "CAN", True)
        return (question, 1, pattern, subject_final)

    def process(self, input_interface):
        # Needs subjects
        logging.info("Start submodule %s", self.get_name())
        if not input_interface.has_subjects():
            return input_interface

        # Read questions
        questions = self._read_questions()
        # Remove question mark at the end
        questions = [re.sub("\?", "", x) for x in questions]
        logging.info("There are " + str(len(questions)) + " questions")
        # Filter questions
        # TODO: what to do with negatives?
        bad_words = ["i", "this", "your", "you", "this", "that", "it", "me",
                     "him", "her", "them", "us", "we", "they", "my", "their",
                     "our", "mine", "yours", "there", "not", "doesn't",
                     "don't", "isn't", "aren't", "he", "she", "those"]
        questions2 = []
        for question in questions:
            bad = False
            for word in question.split(" "):
                if word in bad_words:
                    bad = True
                    break
            if not bad:
                questions2.append(question)
        questions = questions2
        logging.info("There are " + str(len(questions)) + " questions after filtering")

        # Create the suggestions
        # A suggestion is (question, rank (low is better), pattern, subject)
        subjects = input_interface.get_subjects()
        # Preprocess subjects
        subjects = [(x.get(), _plural_engine.plural(x.get()))
                    for x in subjects]
        d_subj = dict()
        for subj in subjects:
            temp = subj[0].split(" ")[0]
            if temp in d_subj:
                d_subj[temp].append(subj)
            else:
                d_subj[temp] = [subj]
            temp1 = subj[1].split(" ")[0]
            if temp1 != temp:
                if temp1 in d_subj:
                    d_subj[temp1].append(subj)
                else:
                    d_subj[temp1] = [subj]
        suggestions = [self._to_suggestion(question, d_subj)
                       for question in questions]
        # Remove unknown subjects
        suggestions = [x for x in suggestions if x[3] != ""]
        logging.info("There are " + str(len(suggestions)) + " questions after subject filtering")

        # OPENIE part
        generated_facts = self.get_generated_facts(suggestions, input_interface)

        return input_interface.add_generated_facts(generated_facts)
