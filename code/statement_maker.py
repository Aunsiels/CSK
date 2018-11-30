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

    def to_statement(self, question, subject):
        subject2 = _plural_engine.plural(subject)
        if question.strip() in self._q2s:
            return self._q2s[question.strip()]
        tokens = []
        pos = []
        statement = ""
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
        if tokens[1] == "are" or tokens[1] == "is":
            found_noun = False
            found_second = False
            found_something_else = False
            found_final_adj = False
            found_cc = False
            found_in = False
            for p in pos[2:]:
                if not found_noun and \
                        ((subject in " ".join(begin) + " " + p[0] or \
                         subject2 in " ".join(begin) + " " + p[0]) \
                         and (not found_cc or "NN" in p[1] or "VBZ" in p[1])):
                    found_noun = True
                    begin.append(p[0])
                elif found_noun and not found_something_else and \
                        not found_second and ("CC" in p[1] or "of" == p[0]):
                    found_cc = True
                    found_noun = False
                    begin.append(p[0])
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
            else:
                statement = " ".join(begin) + " have " + " ".join(middle) + \
                    " " +\
                    " ".join(end)
        # elif (tokens[1] == "do" or tokens[1] == "does") and\
        #         (tokens[2] == "n't" or tokens[2] == "not"):
        #     # Transformation into positive
        #     # TODO CAREFUL HERE if no pattern
        #     statement = " ".join(tokens[3:])
        elif tokens[1] == "do" or tokens[1] == "does":
            statement = " ".join(tokens[2:])
        elif tokens[1] == "can" or tokens[1] == "could" or \
                tokens[1] == "cannot":
            # Look for first verb, in base form
            for i in range(len(pos)):
                p = pos[i]
                if p[1] == "VBP" or p[1] == "VB":
                    statement = " ".join(tokens[2:i]) + " " + tokens[1] + " " +\
                        " ".join(tokens[i:])
                    break
        elif tokens[1] == "ca" and tokens[2] == "n't":
            # I have to turn it to an affirmation to make openIE work
            temp = self.to_statement(tokens[0] + " can " +
                                      " ".join(tokens[3:]), subject)
            statement = temp
            # return temp.replace(" can ", " cannot ")
        else:
            statement = question
        self._save_q2s(question, statement, subject)
        return statement
