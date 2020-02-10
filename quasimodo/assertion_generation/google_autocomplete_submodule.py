import json
import logging
import time
from urllib.parse import quote

import requests

from quasimodo.cache.cachable_querying_system import CachableQueryingSystem
from quasimodo.cache.mongodb_cache import MongoDBCache
from quasimodo.parameters_reader import ParametersReader
from quasimodo.assertion_generation.browser_autocomplete_submodule import BrowserAutocompleteSubmodule


parameters_reader = ParametersReader()
PATTERN_FIRST = (parameters_reader.get_parameter("pattern-first") or "true") == "true"

headers = {'User-agent': 'Mozilla/5.0'}
# baseurl = "http://clients1.google.com/complete/search?"
baseurl = "http://google.com/complete/search?"
RELOADTIME = 60

# Look for new sentences?
look_new = not PATTERN_FIRST

DEFAULT_MONGODB_LOCATION = parameters_reader.get_parameter("default-mongodb-location") or "mongodb://localhost:27017/"


class GoogleAutocompleteSubmodule(BrowserAutocompleteSubmodule, CachableQueryingSystem):
    """SubmoduleGoogleAutocomplete
    A submodule for the google autocomplete triple generation
    """

    def __init__(self, module_reference, use_cache=True, cache_name="google-cache"):
        BrowserAutocompleteSubmodule.__init__(self, module_reference)
        CachableQueryingSystem.__init__(self, MongoDBCache(cache_name, mongodb_location=DEFAULT_MONGODB_LOCATION))
        self._name = "Google Autocomplete"
        self.use_cache = use_cache
        self.time_between_queries = 1.0
        self.default_number_suggestions = 10

    def clean(self):
        super(GoogleAutocompleteSubmodule, self).clean()
        del self.local_cache
        self.local_cache = {}

    def get_suggestion(self, query, lang="en", ds=''):
        """Query Google suggest service"""
        if self.use_cache:
            cache_value = self.read_cache(query)
            if cache_value is not None:
                suggestions, is_cached = cache_value
                suggestions = [[suggestion[0], float(suggestion[1])] for suggestion in suggestions if suggestion[0] != query.strip()]
                return suggestions, is_cached
        if not look_new or not query:
            return None, False
        response = get_request(query, ds, lang)
        return self.get_suggestions_from_response(response, query, ds, lang)

    def get_suggestions_from_response(self, response, query, ds, lang):
        if response.ok:
            begin_time = time.time()
            result = json.loads(response.content.decode("utf-8"))
            suggestions = [[result[1][ranking], ranking] for ranking in range(len(result[1])) if result[1][ranking] != query.strip()]
            if self.use_cache:
                self.write_cache(query, suggestions)
            # We sleep only if the data was not cached
            time.sleep(max([0, self.time_between_queries - (time.time() - begin_time)]))
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
