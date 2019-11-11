import sys
from string import ascii_lowercase
import logging
from flask import Flask

from quasimodo.default_module_factory import DefaultModuleFactory
from quasimodo.inputs import Inputs

LIMIT_DEPTH = 2

PATTERN_FIRST = True


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def get_all_queries(input_interface):
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
                if len(current_state) >= LIMIT_DEPTH:
                    continue
                new_query = (base_query + " " + "".join(current_state)).strip()
                yield new_query
                # We go deeper
                for c in ascii_lowercase:
                    to_process.append(current_state[:] + [c])


# Generate inputs
default_module_factory = DefaultModuleFactory()
seeds = default_module_factory.get_module("all-seeds")
inputs = Inputs([], [], [], [], [])
inputs = seeds.process(inputs)
patterns = default_module_factory.get_module("patterns")
inputs = patterns.process(inputs)

# Get query generator
query_generator = get_all_queries(inputs)


def get_next_query():
    try:
        return query_generator.__next__()
    except StopIteration:
        return ""


# Start Server
app = Flask(__name__)


@app.route("/get_query")
def get_query():
    return get_next_query()


if __name__ == "__main__":
    app.run()