import json
import logging
import sys
import time
from urllib.parse import quote

import requests

from quasimodo.cachable_querying_system import CachableQueryingSystem
from quasimodo.mongodb_cache import MongoDBCache
from quasimodo.parameters_reader import ParametersReader


headers = {'User-agent': 'Mozilla/5.0'}
# baseurl = "http://clients1.google.com/complete/search?"
baseurl = "http://google.com/complete/search?"
RELOADTIME = 60

# Look for new sentences?
look_new = True

parameters_reader = ParametersReader()
DEFAULT_MONGODB_LOCATION = parameters_reader.get_parameter("default-mongodb-location") or "mongodb://localhost:27017/"
SERVER_URL = parameters_reader.get_parameter("server-url") or "http://localhost:5000/get_query"


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class GoogleAutocompleteClient(CachableQueryingSystem):
    """SubmoduleGoogleAutocomplete
    A submodule for the google autocomplete triple generation
    """

    def __init__(self, use_cache=True, cache_name="google-cache"):
        CachableQueryingSystem.__init__(self, MongoDBCache(cache_name, mongodb_location=DEFAULT_MONGODB_LOCATION))
        self._name = "Google Autocomplete"
        self.use_cache = use_cache
        self.time_between_queries = 1.0
        self.default_number_suggestions = 10
        self.begin_time = time.time()

    def get_suggestion(self, query, lang="en", ds=''):
        """Query Google suggest service"""
        if self.use_cache:
            cache_value = self.read_cache(query)
            if cache_value is not None:
                suggestions, is_cached = cache_value
                suggestions = [(suggestion[0], float(suggestion[1])) for suggestion in suggestions]
                return suggestions, is_cached
        if not look_new or not query:
            return None, False
        # We sleep only if the data was not cached
        time.sleep(max([0, self.time_between_queries - (time.time() - self.begin_time)]))
        response = get_request(query, ds, lang)
        self.begin_time = time.time()
        return self.get_suggestions_from_response(response, query, ds, lang)

    def get_suggestions_from_response(self, response, query, ds, lang):
        if response.ok:
            result = json.loads(response.content.decode("utf-8"))
            suggestions = [(result[1][ranking], ranking) for ranking in range(len(result[1]))]
            if self.use_cache:
                self.write_cache(query, suggestions)
            return suggestions, False
        else:
            # Kicked by the search engine
            logging.warning("The number of requests for the google autocomplete submodule was probably exceeded")
            time.sleep(RELOADTIME)
            return self.get_suggestion(query, lang, ds)


def get_request(query, ds, language):
    formatted_query = quote(query)
    url = baseurl + "hl=%s&q=%s&json=t&ds=%s&client=serp" % (language, formatted_query, ds)
    response = requests.get(url, headers=headers)
    return response


client = GoogleAutocompleteClient()


def get_new_query():
    response = requests.get(SERVER_URL)
    return response.content.decode("utf-8")


while True:
    query = get_new_query()
    if query:
        print("Getting", query)
        client.get_suggestion(query)
