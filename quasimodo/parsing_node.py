class ParsingNode:

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
        new_node = ParsingNode()
        self.nexts[symbol] = new_node

    def create_terminal_node(self, word):
        self.is_terminal = True
        self.value = word

    def get_next_node(self, character):
        return self.nexts.get(character, None)

    def add_sentence(self, sentence):
        sentence_split = sentence.split(" ")
        for word in sentence_split:
            self.add_with_return_begin(word, self)

    def add_with_return_begin(self, remaining, final_node):
        self.initialize_or_increase_value()
        if len(remaining) == 0:
            if " " not in self.nexts:
                self.nexts[" "] = final_node
        else:
            self._create_transition_to_new_node_if_required(remaining)
            self.add_to_next_node_with_return_begin(remaining, final_node)

    def initialize_or_increase_value(self):
        if self.value is None:
            self.value = 1
        else:
            self.value += 1

    def add_to_next_node_with_return_begin(self, remaining, final_node):
        self.nexts[remaining[0]].add_with_return_begin(remaining[1:], final_node)

    def read_word(self, word):
        if len(word) == 0:
            return self
        if word[0] in self.nexts:
            return self.nexts[word[0]].read_word(word[1:])
        return None