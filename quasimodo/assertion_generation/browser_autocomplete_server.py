from queue import Queue, Empty
import sys
import logging
from flask import Flask, request

from quasimodo.default_module_factory import DefaultModuleFactory
from quasimodo.data_structures.inputs import Inputs

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
            yield base_query + " "


# Generate inputs
default_module_factory = DefaultModuleFactory()
seeds = default_module_factory.get_module("all-seeds")
inputs = Inputs([], [], [], [], [])
inputs = seeds.process(inputs)
patterns = default_module_factory.get_module("patterns")
inputs = patterns.process(inputs)

# Get query generator
query_generator = get_all_queries(inputs)


query_queue = Queue()
for query in query_generator:
    query_queue.put(query)


# Start Server
app = Flask(__name__)

@app.route("/")
def get_hello():
    return "Hello world"


@app.route("/get_query")
def get_query():
    try:
        return query_queue.get_nowait()
    except Empty:
        return ""


@app.route("/add_new", methods=["POST"])
def add_new():
    data = request.get_json()
    for new_query in data["new_queries"]:
        query_queue.put(new_query)
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1050)
