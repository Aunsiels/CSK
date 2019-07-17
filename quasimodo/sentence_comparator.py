import logging

from quasimodo.content_comparator import ContentComparator
from quasimodo.only_subject_submodule import get_subjects_in_all_forms


def get_parsing_tree(subjects):
    root = Node()
    for subject in subjects:
        root.add(subject)
    return root


class SentenceComparator(ContentComparator):

    def __init__(self, module_reference, filename):
        super().__init__(module_reference)
        self.subjects = []
        self.variations = dict()
        self.parsing_tree = None
        self.filename = filename
        self.per_subject = dict()
        self._name = "Sentence Comparator"

    def setup_processing(self, input_interface):
        if len(self.filename) == 0:
            return
        self.per_subject = dict()
        logging.info("Constructing parsing tree...")
        self.subjects, self.variations = get_subjects_in_all_forms(input_interface)
        self.parsing_tree = get_parsing_tree(self.subjects)
        logging.info("Reading sentence file...")
        with open(self.filename) as f:
            for line in f:
                self.add_line_to_corresponding_subjects(line)
        logging.info("End of preprocessing")

    def add_line_to_corresponding_subjects(self, line):
        current_nodes = [self.parsing_tree]
        line = line.strip()
        for character in line:
            next_nodes = self.process_character_in_line_and_add_subject_if_necessary(character, current_nodes, line)
            current_nodes = next_nodes

    def process_character_in_line_and_add_subject_if_necessary(self, character, current_nodes, line):
        next_nodes = []
        for node in current_nodes:
            next_node = node.get_next_node(character)
            if next_node is not None:
                next_nodes.append(next_node)
                if next_node.is_terminal:
                    self.process_terminal_node(line, next_node)
        if character == " ":
            next_nodes.append(self.parsing_tree)
        return next_nodes

    def process_terminal_node(self, line, next_node):
        subject = self.variations[next_node.value]
        if subject not in self.per_subject:
            self.per_subject[subject] = set()
        self.per_subject[subject].add(line)

    def get_contents(self, subject):
        if len(self.filename) == 0:
            return []
        return self.per_subject.get(subject, [])


class Node:

    def __init__(self):
        self.nexts = dict()
        self.is_terminal = False
        self.value = None

    def add(self, word):
        self.add_with_final_value(word, word)

    def add_with_final_value(self, final_value, remaining):
        if len(remaining) == 0:
            self.create_terminal_node(final_value)
        else:
            self._create_transition_to_new_node_if_required(remaining)
            self._add_to_next_node(remaining, final_value)

    def _add_to_next_node(self, remaining, word):
        self.nexts[remaining[0]].add_with_final_value(word, remaining[1:])

    def _create_transition_to_new_node_if_required(self, remaining):
        if remaining[0] not in self.nexts:
            self._create_transition_to_new_node(remaining[0])

    def _create_transition_to_new_node(self, symbol):
        new_node = Node()
        self.nexts[symbol] = new_node

    def create_terminal_node(self, word):
        self.is_terminal = True
        self.value = word

    def get_next_node(self, character):
        return self.nexts.get(character, None)
