import os

import inflect

from quasimodo.parameters_reader import ParametersReader

NON_PLURAL = ["texas", "star wars", "gas", "people", "chaos", "fetus", "moses",
              "jesus", "gps", "abs", "sos", "mars", "jeans", "https"]


parameters_reader = ParametersReader()
FILENAME = parameters_reader.get_parameter("wikidata-subjects") or \
        os.path.dirname(__file__) + "/data/wikidata.txt"


class InflectAccessor:

    def __init__(self):
        self._conversions_singular = dict()
        self._conversions_plural = dict()
        self._plural_engine = inflect.engine()
        self._proper_name = set()
        with open(FILENAME) as f:
            for line in f:
                self._proper_name.add(line.strip().lower())

    def to_singular(self, word):
        if word in self._conversions_singular:
            return self._conversions_singular[word]
        singular = self._plural_engine.singular_noun(word)
        if not singular or word in NON_PLURAL or word.endswith("sis") or \
                word in self._proper_name:
            self._conversions_singular[word] = word
        else:
            self._conversions_singular[word] = singular
        return self._conversions_singular[word]

    def to_plural(self, word):
        if word in self._conversions_plural:
            return self._conversions_plural[word]
        plural = self._plural_engine.plural(word)
        self._conversions_plural[word] = plural
        return plural


DEFAULT_INFLECT = InflectAccessor()
