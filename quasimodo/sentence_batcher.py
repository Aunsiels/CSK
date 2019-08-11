from typing import Iterator, List, Any


class SentenceBatcher(Iterator):

    def __init__(self, sentences, max_size, size_function):
        self._sentences = sentences
        self._max_size = max_size
        self._size_function = size_function
        self._current_index_iteration = 0

    def __iter__(self):
        self._current_index_iteration = 0
        return self

    def __next__(self) -> List[Any]:
        if self._current_index_iteration >= len(self._sentences):
            raise StopIteration
        total_size = 0
        initial_index = self._current_index_iteration
        while total_size < self._max_size and self._current_index_iteration < len(self._sentences):
            total_size += self._size_function(self._sentences[self._current_index_iteration])
            self._current_index_iteration += 1
        if total_size >= self._max_size:
            self._current_index_iteration -= 1
        if self._current_index_iteration == initial_index:
            raise TooLongBatchException("The " + str(initial_index) + " index is too long.")
        return self._sentences[initial_index:self._current_index_iteration]


class TooLongBatchException(Exception):

    def __init__(self, message):
        self.message = message