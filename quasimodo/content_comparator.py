import logging

import nltk
from nltk.stem import WordNetLemmatizer

from quasimodo.submodule_interface import SubmoduleInterface
from quasimodo.parsing_node import ParsingNode

MAX_SIZE_TO_LOOK_FOR = 6

lemmatizer = WordNetLemmatizer()

def lemmatize_contents(contents):
    for i in range(len(contents)):
        if contents[i] is not None:
            contents[i] = lemmatize(contents[i].lower())


def negate_modal(predicate):
    predicate += " not"
    return predicate


def negate_general_predicate(predicate):
    predicate = "do not " + predicate
    return predicate


def negate_can(predicate_split):
    predicate = "cannot"
    if len(predicate_split) > 1:
        predicate += " " + " ".join(predicate_split[1:])
    return predicate


def get_property_predicate():
    predicate = "are"
    return predicate


def group_by_subject(generated_facts):
    by_subject = dict()
    for g in generated_facts:
        subj = g.get_subject().get().lower()
        if subj in by_subject:
            by_subject[subj].append(g)
        else:
            by_subject[subj] = [g]
    return by_subject


def negate_predicate(predicate):
    predicate_split = predicate.split(" ")
    if predicate_split[0] == "are":
        predicate = negate_modal(predicate)
    elif predicate_split[0] == "can":
        predicate = negate_can(predicate_split)
    else:
        predicate = negate_general_predicate(predicate)
    return predicate


def get_object_as_string(generated_fact):
    obj = generated_fact.get_object().get().lower()
    return obj


def get_predicate_as_string(generated_fact):
    predicate = generated_fact.get_predicate().get().lower()
    is_a_property = predicate.startswith("has_") or predicate == "hasProperty"
    if is_a_property:
        predicate = get_property_predicate()
    is_negative = generated_fact.is_negative()
    if is_negative:
        predicate = negate_predicate(predicate)
    return predicate


def get_part_to_find_in_content(generated_fact):
    obj = get_object_as_string(generated_fact)
    predicate = get_predicate_as_string(generated_fact)
    return lemmatize(predicate + " " + obj)


def get_score_generated_fact_given_lemmatized_content(lemmatized_content, generated_fact):
    part_to_find = get_part_to_find_in_content(generated_fact)
    score = 0
    counter = 0
    part_to_find = part_to_find.split(" ")
    for i in range(len(part_to_find)):
        for j in range(i + 1, min(i + MAX_SIZE_TO_LOOK_FOR + 1, len(part_to_find) + 1)):
            po_temp = " ".join(part_to_find[i:j])
            counter += j - i
            if po_temp in lemmatized_content:
                score += j - i
    score /= counter
    return score


def get_score_generated_fact_given_all_contents(generated_fact, contents):
    scores = []
    for content in contents:
        scores.append(get_score_generated_fact_given_lemmatized_content(content, generated_fact))
    return compute_final_score(scores)


def compute_final_score(scores):
    if scores:
        final_score = sum(scores) / len(scores)
    else:
        final_score = 0
    return final_score


def get_score_generated_fact_given_parsing_node(generated_fact, parsing_node):
    if parsing_node.value is None:
        logging.info("No content found for " + str(generated_fact.get_subject().get()))
        return 0.0
    part_to_find = get_part_to_find_in_content(generated_fact)
    score = 0
    counter = 0
    part_to_find = part_to_find.split(" ")
    for i in range(len(part_to_find)):
        for j in range(i + 1, min(i + MAX_SIZE_TO_LOOK_FOR + 1, len(part_to_find) + 1)):
            po_temp = " ".join(part_to_find[i:j])
            counter += (j - i) * parsing_node.value
            final_node = parsing_node.read_word(po_temp)
            if final_node is not None:
                score += (j - i) * final_node.value
    score /= counter
    return score


class ContentComparator(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference

    def process(self, input_interface):
        logging.info("Start the wikipedia cooccurrence checking")
        while True:
            try:
                self.setup_processing(input_interface)
                break
            except OSError as e:
                logging.info("Failed to setup the content comparator, " + str(e))
        generated_facts = input_interface.get_generated_facts()
        by_subject = group_by_subject(generated_facts)
        n_subjects = len(by_subject.keys())
        counter = 0
        for subject in by_subject:
            if counter % 1000 == 0:
                logging.info("%d done over %d", counter, n_subjects)
            counter += 1
            try:
                contents = self.get_contents(subject)
                contents = [x for x in contents if x is not None]
            except Exception as e:
                logging.info("Problem with " + subject + " " + str(e))
                continue
            lemmatize_contents(contents)
            parsing_node = self.create_parsing_node_from_contents(contents)
            for generated_fact in by_subject[subject]:
                final_score = get_score_generated_fact_given_parsing_node(generated_fact, parsing_node)
                generated_fact.get_score().add_score(final_score, self._module_reference, self)
        return input_interface

    def create_parsing_node_from_contents(self, contents):
        parsing_node = ParsingNode()
        for content in contents:
            parsing_node.add_sentence(content)
        return parsing_node

    def setup_processing(self, input_interface):
        raise NotImplementedError

    def get_contents(self, subject):
        raise NotImplementedError


def lemmatize(s):
    return " ".join([lemmatizer.lemmatize(x) for x in nltk.word_tokenize(s)])
