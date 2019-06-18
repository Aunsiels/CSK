import requests
from urllib.parse import quote
import json
import logging
import time

from quasimodo.mongodb_cache import MongoDBCache
from quasimodo.parameters_reader import ParametersReader
from .browser_autocomplete_submodule import BrowserAutocompleteSubmodule

headers = {'User-agent': 'Mozilla/5.0'}
# baseurl = "http://clients1.google.com/complete/search?"
baseurl = "http://google.com/complete/search?"
RELOADTIME = 60

# Look for new sentences?
look_new = True

parameters_reader = ParametersReader()
DEFAULT_MONGODB_LOCATION = parameters_reader.get_parameter("default-mongodb-location") or "mongodb://localhost:27017/"


def get_request(query, ds, language):
    formatted_query = quote(query)
    url = baseurl + "hl=%s&q=%s&json=t&ds=%s&client=serp" % (language, formatted_query, ds)
    response = requests.get(url, headers=headers)
    return response


def get_regex_from_query(filename):
    # Remove the pattern to be get more results
    filename_split = filename.split("-")
    if len(filename_split) <= 1:
        filename_regex = filename
    else:
        if filename_split[0] in ["why", "how"]:
            if filename_split[1] in ["is", "are", "do", "does", "can", "can_t"] and len(filename_split) >= 3:
                if filename_split[2][-1] == "s":
                    filename_split[2] = filename_split[2][:-1]
                filename_regex = "-".join(filename_split[2:])
            else:
                filename_regex = "-".join(filename_split[1:])
        else:
            filename_regex = filename
    return filename_regex


class GoogleAutocompleteSubmodule(BrowserAutocompleteSubmodule):
    """SubmoduleGoogleAutocomplete
    A submodule for the google autocomplete triple generation
    """

    def __init__(self, module_reference, use_cache=True, cache_name="google-cache"):
        super().__init__(module_reference)
        self._name = "Google Autocomplete"
        self.use_cache = use_cache
        self.cache = MongoDBCache(cache_name, mongodb_location=DEFAULT_MONGODB_LOCATION)
        self.time_between_queries = 1.0
        self.default_number_suggestions = 10
        self.local_cache = {}

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
        response = get_request(query, ds, lang)
        return self.get_suggestions_from_response(response, query, ds, lang)

    def get_suggestions_from_response(self, response, query, ds, lang):
        if response.ok:
            begin_time = time.time()
            result = json.loads(response.content.decode("utf-8"))
            suggestions = [(result[1][ranking], ranking) for ranking in range(len(result[1]))]
            if self.use_cache:
                self.write_cache(query, suggestions)
            # We sleep only if the data was not cached
            time.sleep(max(0, self.time_between_queries - (time.time() - begin_time)))
            return suggestions, False
        else:
            # Kicked by the search engine
            logging.warning("The number of requests for the google autocomplete submodule was probably exceeded")
            time.sleep(RELOADTIME)
            return self.get_suggestion(query, lang, ds)

    def read_cache(self, query):
        filename = query.replace(" ", "-").replace("'", "_").replace("/", "-")
        if filename in self.local_cache:
            return self.local_cache[filename], True
        else:
            filename_regex = get_regex_from_query(filename)
            if self.local_cache.get("query_regex", "") != filename_regex:
                self.local_cache = self.cache.read_regex(filename_regex)
                self.local_cache["query_regex"] = filename_regex
        if filename in self.local_cache:
            return self.local_cache[filename], True
        return None

    def write_cache(self, query, suggestions):
        filename = query.replace(" ", "-").replace("'", "_").replace("/", "-")
        self.cache.write_cache(filename, suggestions)
