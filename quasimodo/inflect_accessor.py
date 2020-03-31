import inflect

NON_PLURAL = ["texas", "star wars", "gas", "people", "chaos", "fetus", "moses",
              "jesus", "gps", "abs", "sos", "mars", "jeans"]


class InflectAccessor:

    def __init__(self):
        self._conversions_singular = dict()
        self._conversions_plural = dict()
        self._plural_engine = inflect.engine()

    def to_singular(self, word):
        if word in self._conversions_singular:
            return self._conversions_singular[word]
        singular = self._plural_engine.singular_noun(word)
        if not singular or word in NON_PLURAL or word.endswith("sis"):
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
