from string import ascii_lowercase
import logging

from quasimodo.parameters_reader import ParametersReader
from .openie_fact_generator_submodule import OpenIEFactGeneratorSubmodule

RANK = 1

SUGGESTION = 0

LIMIT_DEPTH = 2

parameters_reader = ParametersReader()
PATTERN_FIRST = (parameters_reader.get_parameter("pattern-first") or "true") == "true"
look_new = not PATTERN_FIRST


def get_base_sentences(base_suggestions):
    return list(map(lambda ranked_suggestion: ranked_suggestion[SUGGESTION],
                    base_suggestions))


class BrowserAutocompleteSubmodule(OpenIEFactGeneratorSubmodule):
    """BrowserAutocompleteSubmodule
    Represents the autocomplete from a web search engine
    """

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self.time_between_queries = 1.0  # The time between two queries
        self.default_number_suggestions = 8  # The maximum number of suggestions

    def get_suggestion(self, query, lang="en", ds=""):
        """get_suggestion
        Gets suggestion from the browser to a give query
        :param query: the query to autocomplete
        :type query: str
        :param lang: the language to use
        :type lang: str
        :param ds: An additional parameter
        :type ds: str
        :return: A list of scored autosuggestions with a whether the cache was
        used or not
        :rtype: List[((str, float), bool)]
        """
        raise NotImplementedError

    def _get_all_suggestions(self, input_interface):
        suggestions = []
        if PATTERN_FIRST:
            collection_first = input_interface.get_patterns("google-autocomplete")
            collection_second = input_interface.get_subjects()
        else:
            collection_first = input_interface.get_subjects()
            collection_second = input_interface.get_patterns("google-autocomplete")
        for i, first_collection_element in enumerate(collection_first):
            if PATTERN_FIRST:
                logging.info("Going for pattern " + str(first_collection_element) +
                             "[" + str(i / len(collection_first) * 100.0) + "%]")
            else:
                logging.info("Going for subject " + str(first_collection_element) +
                             "[" + str(i / len(collection_first) * 100.0) + "%]")
            for second_collection_element in collection_second:
                if PATTERN_FIRST:
                    pattern = first_collection_element
                    subject = second_collection_element
                else:
                    pattern = second_collection_element
                    subject = first_collection_element
                # Generate the query
                base_query = pattern.to_str_subject(subject)
                base_sentences = []
                # Artificially add more suggestions
                to_process = [[]]
                while to_process:
                    current_state = to_process.pop()
                    if len(current_state) >= LIMIT_DEPTH and look_new:
                        continue
                    new_query = (base_query + " " + "".join(current_state)).strip()
                    base_suggestions, cache = self.get_suggestion(new_query)
                    if base_suggestions is None:
                        continue
                    if len(base_suggestions) == self.default_number_suggestions:
                        # We go deeper
                        to_append = list(ascii_lowercase)
                        if current_state and current_state[-1] != " ":
                            to_append.append(" ")
                        for c in to_append:
                            to_process.append(current_state[:] + [c])
                    suggestions += self.clean_suggestions(base_suggestions, base_sentences, current_state,
                                                          pattern, subject)
                    base_sentences += get_base_sentences(base_suggestions)
                    if base_suggestions is None:
                        continue
        return suggestions

    def clean_suggestions(self, base_suggestions, base_sentences, new_state, pattern, subject):
        base_suggestions = filter(
            lambda ranked_suggestion: ranked_suggestion[SUGGESTION] not in base_sentences,
            base_suggestions)
        base_suggestions = map(
            lambda ranked_suggestion:
            (ranked_suggestion[SUGGESTION],
             ranked_suggestion[RANK] + len(new_state) * self.default_number_suggestions,
             pattern, subject.get()), base_suggestions)
        base_suggestions = list(
            filter(lambda ranked_suggestion: pattern.match(ranked_suggestion[SUGGESTION]),
                   base_suggestions))
        return base_suggestions

    def process(self, input_interface):
        # Needs subjects
        logging.info("Start submodule %s", self.get_name())
        if not input_interface.has_subjects():
            return input_interface

        suggestions = self._get_all_suggestions(input_interface)

        logging.info("We collected " + str(len(suggestions)) + " suggestions.")

        # OPENIE part
        generated_facts_bis = self._openie_from_file(suggestions)
        generated_facts = self.get_generated_facts(suggestions)

        return input_interface.add_generated_facts(generated_facts_bis).add_generated_facts(generated_facts)
