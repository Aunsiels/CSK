import os
import logging

from quasimodo.parameters_reader import ParametersReader

filename = None

parameters_reader = ParametersReader()
filename = parameters_reader.get_parameter("openie-file") or None
filename_no_found = parameters_reader.get_parameter("openie-file-no-found") or\
        os.path.dirname(__file__) + "/data/no_found_openie_sentences.txt"


class OpenIEReader(object):

    def __init__(self):
        self.sentence_to_fact = dict()
        if filename is not None:
            self.initialize_from_filename()

    def initialize_from_filename(self):
        with open(filename) as f:
            temp = []
            sentence = ''
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    if sentence != "":
                        self.sentence_to_fact[sentence] = temp
                    temp = []
                    sentence = ""
                else:
                    if sentence != "":
                        fact = read_fact(line)
                        if fact is not None:
                            temp.append(fact)
                    else:
                        sentence = line
            if sentence != "":
                self.sentence_to_fact[sentence] = temp

    def get_from_sentence(self, sentence):
        if sentence in self.sentence_to_fact:
            return self.sentence_to_fact[sentence]
        else:
            while True:
                try:
                    with open(filename_no_found, "a") as f:
                        f.write(sentence + "\n")
                        break
                except:
                    logging.info("Error while writting the sentence in openie_reader")
            return []


def read_fact(line):
    if "Context" in line:
        return None
    line = line.strip()
    temp = line.split(" (")
    if len(temp) != 2 or temp[1].startswith("Context"):
        return None
    score = temp[0].strip()
    fact = temp[1][:-1].split("; ")
    if len(fact) < 3:
        return None
    subject = fact[0]
    predicate = fact[1]
    obj = []
    for element in fact[2:]:
        element = element.strip()
        if len(element) != 0:
            if element.startswith("L:") or element.startswith("T:"):
                obj.append(element[2:])
            else:
                obj.append(element)
    return [subject, predicate, " ".join(obj), score]

