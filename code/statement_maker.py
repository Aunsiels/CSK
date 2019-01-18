import os
import spacy
import inflect


_plural_engine = inflect.engine()
_nlp = spacy.load('en_core_web_sm')

class StatementMaker(object):

    def __init__(self):
        self._cache_dir = "question2statement/"
        self._filename = "cache.tsv"
        if not os.path.exists(self._cache_dir):
            os.makedirs(self._cache_dir)
        # Load previous q2s
        self._q2s = dict()
        self._load_q2s()


    def _load_q2s(self):
        if os.path.isfile(self._cache_dir + self._filename):
            with open(self._cache_dir + self._filename) as f:
                for line in f:
                    line = line.strip().split("\t")
                    if len(line) < 2:
                        continue
                    self._q2s[line[0]] = line[1]

    def _save_q2s(self, question, statement, subject):
        with open(self._cache_dir + self._filename, "a") as f:
            f.write(question.strip() + "\t" + statement.strip() +
                    "\t" + subject + "\n")

    def _correct_tokens(self, tokens, pos):
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

    def to_statement(self, question, subject):
        subject2 = _plural_engine.plural(subject)
        if question.strip() in self._q2s:
            return self._q2s[question.strip()]
        tokens = []
        pos = []
        statement = ""
        question = question.replace(" cant ", " can't ")
        for token in _nlp(question):
            if token.text == "'s":
                tokens[-1] = tokens[-1] + "'s"
                pos[-1] = (pos[-1][0] + "'s", pos[-1][1])
            elif token.text == "?":
                continue
            else:
                tokens.append(token.text)
                pos.append((token.text, token.tag_))
        begin = []
        middle = []
        end = []
        # Correct nano - particule
        tokens, pos = self._correct_tokens(tokens, pos)
        tokens_begin = []
        if (tokens[1] == "are" or tokens[1] == "is" \
                or tokens[1] == "was" or tokens[1] == "were") and \
                len(tokens) == 4:
            statement = " ".join([tokens[2], tokens[1], tokens[3]])
        elif tokens[1] == "are" or tokens[1] == "is" \
                or tokens[1] == "was" or tokens[1] == "were" and\
                tokens[2] in ["there", "it", "i", "they", "she", "he", "we",
                              "you"]:
            statement = " ".join([tokens[2], tokens[1]] + tokens[3:])
        elif tokens[1] == "are" or tokens[1] == "is" \
                or tokens[1] == "was" or tokens[1] == "were":
            found_noun = False
            found_second = False
            found_something_else = False
            found_final_adj = False
            found_cc = False
            found_in = False
            for i in range(2, len(pos)):
                p = pos[i]
                if not found_noun and \
                        ((subject in " ".join(begin) + " " + p[0] or \
                         subject2 in " ".join(begin) + " " + p[0])\
                         and (not found_cc or "NN" in p[1] or "VBZ" in p[1])):
                    if (tokens[1] != "are" or "NNS" == p[1] or found_cc or "CC" in p[1]\
                            or (i != len(pos) -1 and "NN" in p[1] and ("RB" in pos[i+1][1] or "JJ" in pos[i+1][1])))\
                            and (p[1] != "VBG" and p[1] != "DT" and\
                                 ("JJ" not in p[1] or len(pos) < 8)):
                        if "CC" in p[1]:
                            found_cc = True
                        elif found_cc and "NN" in p[1]:
                            found_noun = True
                        elif not found_cc:
                            found_noun = True
                    begin.append(p[0])
                    tokens_begin.append(p[1])
                elif found_noun and not found_something_else and \
                        not found_second and ("CC" in p[1] or "of" == p[0]):
                    found_cc = True
                    found_noun = False
                    begin.append(p[0])
                    tokens_begin.append(p[1])
                elif found_noun and not found_something_else and found_second\
                        and ("CC" in p[1] or "of" == p[0]):
                    found_second = False
                    end.append(p[0])
                elif not found_something_else and found_noun and \
                        ("NN" in p[1] or "IN" in p[0])\
                        and not found_final_adj:
                    if "IN" in p[0]:
                        found_in = True
                    found_second = True
                    end.append(p[0])
                elif not found_noun:
                    begin.append(p[0])
                else:
                    if "JJ" in p[1]:
                        found_final_adj = True
                    found_something_else = True
                    middle.append(p[0])
            if middle and middle[0] == tokens[1]:
                middle = middle[1:]
            if end and end[0] == tokens[1]:
                end = end[1:]
            if begin[-1] == "not":
                begin = begin[:-1]
                middle = ["not"] + middle
            if len(begin) == 0:
                statement = ""
            elif len(middle) == 0 and len(end) == 0:
                statement = ""
            elif len(middle) == 0:
                statement = " ".join(begin) + " " + tokens[1] + \
                    " " + " ".join(end)
            elif len(end) == 0:
                statement =  " ".join(begin) + " " + tokens[1] + " " +\
                    " ".join(middle)
            elif found_in:
                statement = " ".join(begin) + " " + tokens[1] + " " + \
                    " ".join(middle) + \
                    " " + \
                    " ".join(end)
            elif tokens[1] == "are" and "NN" in tokens_begin[-1]\
                    and tokens[0] == "why":
                statement = " ".join(begin) + " have " + " ".join(middle) + \
                    " " +\
                    " ".join(end)
            else:
                mid = " ".join(middle)
                if mid.startswith(tokens[1]+ " "):
                    statement = " ".join(begin) + " " + " ".join(end) + " " + \
                        mid
                else:
                    statement = " ".join(begin) + " " + " ".join(end) + " " + \
                        tokens[1] + " " + mid
        elif tokens[1] == "do" or tokens[1] == "does":
            statement = " ".join(tokens[2:])
        elif tokens[1] == "can" or tokens[1] == "could" or \
                tokens[1] == "cannot":
            if len(tokens) == 4:
                statement = tokens[2] + " " + tokens[1] + " " + tokens[3]
            else:
                # Look for first verb, in base form
                found_noun = False
                for i in range(len(pos)):
                    p = pos[i]
                    if p[1] == "VBP" or p[1] == "VB" and found_noun:
                        statement = " ".join(tokens[2:i]) + " " + tokens[1] + " " +\
                            " ".join(tokens[i:])
                        break
                    elif "NN" in p[1]:
                        found_noun = True
        elif tokens[1] == "ca" and tokens[2] == "n't":
            # I have to turn it to an affirmato_station to make openIE work
            temp = self.to_statement(tokens[0] + " can " +
                                      " ".join(tokens[3:]), subject)
            statement = temp
            # return temp.replace(" can ", " cannot ")
        else:
            statement = question
        self._save_q2s(question, statement, subject)
        return statement
