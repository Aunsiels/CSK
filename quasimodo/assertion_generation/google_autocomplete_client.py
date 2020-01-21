import json
import logging
import sys
import time
from urllib.parse import quote
from string import ascii_lowercase

import requests

from quasimodo.cache.cachable_querying_system import CachableQueryingSystem
from quasimodo.cache.mongodb_cache import MongoDBCache
from quasimodo.parameters_reader import ParametersReader


headers = {'User-agent': 'Mozilla/5.0'}
# baseurl = "http://clients1.google.com/complete/search?"
baseurl = "http://google.com/complete/search?"
RELOADTIME = 600

# Look for new sentences?
look_new = True

parameters_reader = ParametersReader()
DEFAULT_MONGODB_LOCATION = parameters_reader.get_parameter("default-mongodb-location") or "mongodb://localhost:27017/"
SERVER_URL = (parameters_reader.get_parameter("server-url") or "http://localhost:5000/").strip("/")
GET_URL = SERVER_URL + "/get_query"
POST_URL = SERVER_URL + "/add_new"
HEADERS_JSON = {'content-type': 'application/json'}


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class GoogleAutocompleteClient(CachableQueryingSystem):
    """SubmoduleGoogleAutocomplete
    A submodule for the google autocomplete triple generation
    """

    def __init__(self, use_cache=True, cache_name="google-cache"):
        CachableQueryingSystem.__init__(self, MongoDBCache(cache_name, mongodb_location=DEFAULT_MONGODB_LOCATION))
        self._name = "Google Autocomplete"
        self.use_cache = use_cache
        self.time_between_queries = 1.5
        self.default_number_suggestions = 10
        self.begin_time = time.time()

    def get_suggestion(self, query, lang="en", ds=''):
        """Query Google suggest service"""
        if self.use_cache:
            cache_value = self.read_cache(query.strip())
            if cache_value is not None:
                suggestions, is_cached = cache_value
                suggestions = [(suggestion[0], float(suggestion[1])) for suggestion in suggestions]
                self.create_new_queries(suggestions, query)
                return suggestions, is_cached
        if not look_new or not query.strip():
            return None, False
        # We sleep only if the data was not cached
        time.sleep(max([0, self.time_between_queries - (time.time() - self.begin_time)]))
        response = get_request(query.strip(), ds, lang)
        self.begin_time = time.time()
        return self.get_suggestions_from_response(response, query, ds, lang)

    def get_suggestions_from_response(self, response, query, ds, lang):
        if response.ok:
            result = json.loads(response.content.decode("utf-8"))
            suggestions = [(result[1][ranking], ranking) for ranking in range(len(result[1]))]
            if self.use_cache:
                self.write_cache(query.strip(), suggestions)
            self.create_new_queries(suggestions, query)
            return suggestions, False
        else:
            # Kicked by the search engine
            logging.warning("The number of requests for the google autocomplete submodule was probably exceeded")
            time.sleep(RELOADTIME)
            return self.get_suggestion(query, lang, ds)

    def create_new_queries(self, suggestions, query):
        if len(suggestions) == self.default_number_suggestions:
            to_append = list(ascii_lowercase)
            if query[-1] != " ":
                to_append.append(" ")
            new_queries = []
            for new_char in to_append:
                new_queries.append(query + new_char)
            send_new_queries(new_queries)


def get_request(query, ds, language):
    formatted_query = quote(query)
    url = baseurl + "hl=%s&q=%s&json=t&ds=%s&client=serp" % (language, formatted_query, ds)
    response = requests.get(url, headers=headers)
    return response


client = GoogleAutocompleteClient()


def get_new_query():
    response = requests.get(GET_URL)
    return response.content.decode("utf-8")


def send_new_queries(queries):
    data = {"new_queries": queries}
    requests.post(POST_URL, data=json.dumps(data), headers=HEADERS_JSON)


while True:
    query = get_new_query()
    if query:
        print("Getting", query)
        client.get_suggestion(query)
