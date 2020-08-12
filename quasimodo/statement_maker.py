import os
import spacy
import language_check
import logging
import time
from subprocess import call

from quasimodo.inflect_accessor import DEFAULT_INFLECT
from quasimodo.parameters_reader import ParametersReader

parameters_reader = ParametersReader()
CACHE_DIR = parameters_reader.get_parameter("question-cache-dir") or \
            os.path.dirname(__file__) + "/question2statement/"

_tool = language_check.LanguageTool('en-US')
_nlp = spacy.load('en_core_web_lg')


TEXT = 0
POS = 1


NEGATE_VERB = ["am", "is", "are", "was", "were", "do", "does", "did"
               "should", "must", "would", "may", "have", "has",
               "might", "shall", "will", "could"]


def _correct_tokens(tokens, pos):
    merge_next = False
    res_tokens = []
    res_pos = []
    for i in range(len(tokens)):
        if tokens[i] == "-":
            res_tokens[-1] = res_tokens[-1] + "-"
            res_pos[-1] = (res_pos[-1][0] + "-", res_pos[-1][1])
            merge_next = True
        elif merge_next:
            merge_next = False
            res_tokens[-1] = res_tokens[-1] + tokens[i]
            res_pos[-1] = (res_pos[-1][0] + pos[i][0], pos[i][1])
        else:
            res_tokens.append(tokens[i])
            res_pos.append(pos[i])
    return res_tokens, res_pos


def is_form_of_be(word):
    return word in ["are", "is", "was", "were", "am", "be"]


def is_personal_pronoun(word):
    return word in ["there", "it", "i", "they", "she", "he", "we", "you"]


def is_form_of_can(word):
    return word in ["can", "could", "cannot", "can't"]


def is_form_do_present(word):
    return word in ["do", "does"]


def is_modal_or_auxiliary(word):
    return is_form_of_can(word) or is_form_of_be(word) or is_form_do_present(word) or \
           word in ["should", "must", "would", "may", "did", "have", "has", "might", "shall", "will"] or \
           "n't" in word


def get_pos_and_tokens_from_question(question):
    tokens = []
    pos = []
    for token in _nlp(question):
        if token.text == "'s":
            tokens[-1] = tokens[-1] + "'s"
            pos[-1] = (pos[-1][TEXT] + "'s", pos[-1][POS])
        elif token.text == "?":
            continue
        else:
            tokens.append(token.text)
            pos.append((token.text, token.tag_))
    return pos, tokens


def process_general_be_form(pos, tokens, subject):
    subject_plural = DEFAULT_INFLECT.to_plural(subject)
    begin = []
    middle = []
    end = []
    tokens_begin = []
    found_noun = False
    found_second = False
    found_something_else = False
    found_final_adj = False
    found_cc = False
    found_in = False
    for i in range(2, len(pos)):
        current_text_pos = pos[i]
        subject_appeared = (subject in " ".join(begin) + " " + current_text_pos[TEXT] or
                            subject_plural in " ".join(begin) + " " + current_text_pos[TEXT])
        if not found_noun and subject_appeared and (
                not found_cc or "NN" in current_text_pos[POS] or "VBZ" in current_text_pos[POS]):
            if (tokens[1] != "are" or "NNS" == current_text_pos[1] or found_cc or "CC" in current_text_pos[POS]
                or (i != len(pos) - 1 and "NN" in current_text_pos[POS] and (
                            "RB" in pos[i + 1][POS] or "JJ" in pos[i + 1][POS]))) \
                    and (current_text_pos[POS] != "VBG" and current_text_pos[POS] != "DT" and
                         ("JJ" not in current_text_pos[POS] or len(pos) < 8)):
                if "CC" in current_text_pos[POS]:
                    found_cc = True
                elif found_cc and "NN" in current_text_pos[POS]:
                    found_noun = True
                elif not found_cc:
                    found_noun = True
            begin.append(current_text_pos[TEXT])
            tokens_begin.append(current_text_pos[POS])
        elif found_noun and not found_something_else and \
                not found_second and ("CC" in current_text_pos[POS] or "of" == current_text_pos[TEXT]):
            found_cc = True
            found_noun = False
            begin.append(current_text_pos[TEXT])
            tokens_begin.append(current_text_pos[POS])
        elif found_noun and not found_something_else and found_second \
                and ("CC" in current_text_pos[POS] or "of" == current_text_pos[TEXT]):
            found_second = False
            end.append(current_text_pos[TEXT])
        elif not found_something_else and found_noun and \
                ("NN" in current_text_pos[POS] or "IN" in current_text_pos[0]) \
                and not found_final_adj:
            if "IN" in current_text_pos[TEXT]:
                found_in = True
            found_second = True
            end.append(current_text_pos[TEXT])
        elif not found_noun:
            begin.append(current_text_pos[TEXT])
        else:
            if "JJ" in current_text_pos[POS]:
                found_final_adj = True
            found_something_else = True
            middle.append(current_text_pos[TEXT])
    begin, middle, end = clean_multiple_parts(begin, middle, end, tokens)
    statement = build_statement_from_multiple_parts(begin, middle, end, found_in, tokens, tokens_begin)
    return statement


def clean_multiple_parts(begin, middle, end, tokens):
    if middle and middle[0] == tokens[1]:
        middle = middle[1:]
    if end and end[0] == tokens[1]:
        end = end[1:]
    if begin[-1] == "not":
        begin = begin[:-1]
        middle = ["not"] + middle
    return begin, middle, end


def build_statement_from_multiple_parts(begin, middle, end, found_in, tokens, tokens_begin):
    begin = [x for x in begin if x != tokens[1]]
    if len(begin) == 0:
        statement = ""
    elif len(middle) == 0 and len(end) == 0:
        statement = ""
    elif len(middle) == 0:
        statement = " ".join(begin) + " " + tokens[1] + \
                    " " + " ".join(end)
    elif len(end) == 0:
        statement = " ".join(begin) + " " + tokens[1] + " " + \
                    " ".join(middle)
    elif found_in:
        statement = " ".join(begin) + " " + tokens[1] + " " + \
                    " ".join(middle) + \
                    " " + \
                    " ".join(end)
    elif tokens[1] == "are" and "NN" in tokens_begin[-1] \
            and tokens[0] == "why":
        statement = " ".join(begin) + " have " + " ".join(middle) + \
                    " " + \
                    " ".join(end)
    else:
        mid = " ".join(middle)
        if mid.startswith(tokens[1] + " "):
            statement = " ".join(begin) + " " + " ".join(end) + " " + \
                        mid
        else:
            statement = " ".join(begin) + " " + " ".join(end) + " " + \
                        tokens[1] + " " + mid
    return statement


def process_can_form(pos, tokens):
    statement = ""
    if len(tokens) == 4:
        statement = tokens[2] + " " + tokens[1] + " " + tokens[3]
    else:
        # Look for first verb, in base form
        found_noun = False
        for i in range(len(pos)):
            current_text_pos = pos[i]
            if current_text_pos[1] == "VBP" or current_text_pos[1] == "VB" and found_noun:
                statement = " ".join(tokens[2:i]) + " " + tokens[1] + " " + " ".join(tokens[i:])
                break
            elif "NN" in current_text_pos[1]:
                found_noun = True
    return statement


def correct_statement(statement):
    if len(statement.strip()) == 0:
        return ""
    global _tool
    try:
        matches = _tool.check(statement)
    except:
        try:
            logging.error("Problem with LanguageTools for " + statement)
            time.sleep(60)
            try:
                del _tool
            except NameError:
                pass
            time.sleep(60)
            call(["killall", "java"])
            time.sleep(60)
            try:
                _tool = language_check.LanguageTool('en-US')
            except:
                raise
            return correct_statement(statement)
        except:
            logging.error("Problem with LanguageTools for " + statement)
            raise
    return language_check.correct(statement, matches).lower()


class StatementMaker(object):

    def __init__(self, use_cache=True):
        self._filename = "cache.tsv"
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        self._use_cache = use_cache
        # Load previous q2s
        self._q2s = dict()
        self._load_q2s()

    def _load_q2s(self):
        if not self._use_cache:
            return
        if os.path.isfile(CACHE_DIR + self._filename):
            with open(CACHE_DIR + self._filename) as f:
                for line in f:
                    line = line.strip().split("\t")
                    if len(line) < 2:
                        continue
                    self._q2s[line[0]] = line[1]

    def _save_q2s(self, question, statement, subject):
        if not self._use_cache:
            return
        self._q2s[question] = statement
        with open(CACHE_DIR + self._filename, "a") as f:
            f.write(question.strip() + "\t" + statement.strip() +
                    "\t" + subject + "\n")

    def to_statement(self, question, subject, safe_source=False):
        question = question.replace("&amp;", " & ").replace("&gt;", " > ").replace("&lt;", " < ")
        if question.strip() in self._q2s:
            return self._q2s[question.strip()]
        question = question.replace(" cant ", " can't ")
        pos, tokens = get_pos_and_tokens_from_question(question)
        if len(pos) <= 2:
            return ""
        # Correct nano - particule
        tokens, pos = _correct_tokens(tokens, pos)

        # replace n't by not
        to_negate = None
        negated_verb = None
        for i, token in enumerate(tokens):
            if token == "n't" and i - 1 >= 0 and tokens[i - 1] in NEGATE_VERB:
                to_negate = i - 1
                break
        if to_negate is not None:
            del tokens[to_negate + 1]
            del pos[to_negate + 1]
            negated_verb = tokens[to_negate]

        if is_form_of_be(tokens[1]) and len(tokens) == 4:
            statement = " ".join([tokens[2], tokens[1], tokens[3]])
        elif is_form_of_be(tokens[1]) and is_personal_pronoun(tokens[2]):
            statement = " ".join([tokens[2], tokens[1]] + tokens[3:])
        elif is_form_of_be(tokens[1]):
            statement = process_general_be_form(pos, tokens, subject)
        elif is_form_do_present(tokens[1]):
            statement = " ".join(tokens[2:])
        elif is_form_of_can(tokens[1]):
            statement = process_can_form(pos, tokens)
        elif tokens[1] == "ca" and tokens[2] == "n't":
            statement = self.process_ca_nt(subject, tokens)
        elif not is_modal_or_auxiliary(tokens[1]):
            statement = " ".join(tokens[1:])
        else:
            statement = question

        if negated_verb is not None:
            statement_split = statement.split(" ")
            position_verb = None
            for i, word in enumerate(statement_split):
                if word == negated_verb:
                    position_verb = i
                    break
            if position_verb is not None:
                statement_split.insert(i + 1, "not")
                statement = " ".join(statement_split)

        if not safe_source:
            statement = correct_statement(statement)
        self._save_q2s(question, statement, subject)
        return statement

    def process_ca_nt(self, subject, tokens):
        # I have to turn it to an affirmation to make openIE work
        temp = self.to_statement(tokens[0] + " can " +
                                 " ".join(tokens[3:]), subject)
        statement = temp
        # return temp.replace(" can ", " cannot ")
        return statement
