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
        self.filename = filename
        self.per_subject = dict()
        self._name = "Sentence Comparator"

    def setup_processing(self, input_interface):
        if len(self.filename) == 0:
            return
        self.per_subject = dict()
        subjects, variations = get_subjects_in_all_forms(input_interface)
        logging.info("Constructing parsing tree...")
        parsing_tree = get_parsing_tree(subjects)
        logging.info("Reading sentence file...")
        with open(self.filename) as f:
            for line in f:
                current_nodes = [parsing_tree]
                line = line.strip()
                for character in line:
                    next_nodes = []
                    for node in current_nodes:
                        next_node = node.get_next_node(character)
                        if next_node is not None:
                            next_nodes.append(next_node)
                            if next_node.is_terminal:
                                subject = variations[next_node.value]
                                if subject not in self.per_subject:
                                    self.per_subject[subject] = set()
                                self.per_subject[subject].add(line)
                    if character == " ":
                        next_nodes.append(parsing_tree)
                    current_nodes = next_nodes
        logging.info("End of preprocessing")

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
        self._add(word, word)

    def _add(self, word, remaining):
        if len(remaining) == 0:
            self.create_terminal_node(word)
        else:
            self._create_transition_to_new_node_if_required(remaining)
            self._add_to_next_node(remaining, word)

    def _add_to_next_node(self, remaining, word):
        self.nexts[remaining[0]]._add(word, remaining[1:])

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
