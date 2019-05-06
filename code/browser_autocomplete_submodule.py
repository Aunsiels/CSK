import time
from string import ascii_lowercase
import logging
from openie_fact_generator_submodule import OpenIEFactGeneratorSubmodule


class BrowserAutocompleteSubmodule(OpenIEFactGeneratorSubmodule):
    """BrowserAutocompleteSubmodule
    Represents the autocomplete from a web search engine
    """

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self.time_between_queries = 1.0 # The time between two queries
        self.default_number_suggestions = 8 # The maximum number of suggestions

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

        for pattern in input_interface.get_patterns("google-autocomplete"):
            logging.info("Processing " + pattern.to_str())
            for subject in input_interface.get_subjects():
                temp = ""
                # Generate the query
                base_query = pattern.to_str_subject(subject)
                base_suggestions, cache = self.get_suggestion(base_query)
                # Exceeded number of requests
                if base_suggestions is None:
                    continue
                # Append the patterns
                base_suggestions = list(map(lambda x:
                                            (x[0], x[1], pattern,
                                             subject.get()),
                                            base_suggestions))
                # add to the list of suggestions
                suggestions += list(filter(lambda x: pattern.match(x[0]),
                                           base_suggestions))
                base_sentences = list(map(lambda x: x[0],
                                          base_suggestions))
                if not cache:
                    time.sleep(self.time_between_queries)
                # There might be more suggestions
                if len(base_suggestions) == self.default_number_suggestions:
                    # Artificially add more suggestions
                    # TODO: To this recursively
                    for c in ascii_lowercase:
                        temp, cache = self.get_suggestion(base_query + " " + c)
                        if temp is None:
                            break
                        # Check not seen before
                        temp = list(filter(lambda x: x[0] not in base_sentences,
                                           temp))
                        temp = list(map(lambda x:
                                        (x[0],
                                         x[1] + self.default_number_suggestions,
                                         pattern,
                                         subject.get()), temp))
                        suggestions += list(filter(lambda x:
                                                       pattern.match(x[0]),
                                                   temp))
                        # We sleep only if the data was not cached
                        if not cache:
                            time.sleep(self.time_between_queries)
                    if temp is None:
                        continue
            if temp is None or base_suggestions is None:
                continue
        return suggestions

    def process(self, input_interface):
        # Needs subjects
        logging.info("Start submodule %s", self.get_name())
        if not input_interface.has_subjects():
            return input_interface

        suggestions = self._get_all_suggestions(input_interface)

        logging.info("We collected " + str(len(suggestions)) + " suggestions.")

        # OPENIE part
        generated_facts = self.get_generated_facts(suggestions, input_interface)


        return input_interface.add_generated_facts(generated_facts)
