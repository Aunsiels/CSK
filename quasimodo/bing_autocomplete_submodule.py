from urllib.parse import quote
import http.client, json
import os

from .mongodb_cache import MongoDBCache
from .parameters_reader import ParametersReader
from .browser_autocomplete_submodule import BrowserAutocompleteSubmodule
import logging
import time

parameters_reader = ParametersReader()

OK = 200
DEFAULT_MONGODB_LOCATION = parameters_reader.get_parameter("default-mongodb-location") or "mongodb://localhost:27017/"
subscriptionKey = parameters_reader.get_parameter("bing-key") or ""

# Location of the api
host = 'api.cognitive.microsoft.com'
path = '/bing/v7.0/suggestions'

# language
mkt = 'en-US'


def get_response(query, lang):
    params = '?mkt=' + lang + '&q=' + quote(query)
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", path + params, None, headers)
    response = conn.getresponse()
    return response


class BingAutocompleteSubmodule(BrowserAutocompleteSubmodule):
    """BingAutocompleteSubmodule
    Submodule which generetes assertions using the autocomplete from Bing
    """

    def __init__(self, module_reference, use_cache=True, cache_name="bing-cache", look_new=False):
        super().__init__(module_reference)
        self._name = "Bing Autocomplete"
        self.use_cache = use_cache
        self.cache = MongoDBCache(cache_name, mongodb_location=DEFAULT_MONGODB_LOCATION)
        self.time_between_queries = 0.02
        self.default_number_suggestions = 8
        self.look_new = look_new

    def get_suggestion(self, query, lang="en-US", ds=0):
        "Gets Autosuggest results for a query and returns the information."
        if self.use_cache:
            filename = query.replace(" ", "-").replace("'", "_")
            cache_value = self.cache.read_cache(filename)
            if cache_value is not None:
                suggestions, is_cached = cache_value
                suggestions = [(suggestion[0], float(suggestion[1])) for suggestion in suggestions]
                return suggestions, is_cached
        if not self.look_new or not query:
            return None, False
        response = get_response(query, lang)
        return self.process_response(response, query, lang, ds)

    def process_response(self, response, query, lang, ds):
        if response.status == OK:
            begin_time = time.time()
            res_json = json.loads(response.read())
            suggestions_temp = []
            for suggestion_group in res_json.setdefault("suggestionGroups", []):
                search_suggestions = suggestion_group.setdefault("searchSuggestions", [])
                for suggestion in search_suggestions:
                    suggestions_temp.append(suggestion.setdefault("query", ""))
            suggestions = [(suggestions_temp[i], i) for i in range(len(suggestions_temp))]
            if self.use_cache:
                filename = query.replace(" ", "-").replace("'", "_")
                self.cache.write_cache(filename, suggestions)
            time.sleep(max(0, self.time_between_queries - (time.time() - begin_time)))
            return suggestions, False
        else:
            # We surely exceeded the number of requests
            logging.warning("The number of requests for the bing autocomplete" +
                            " submodule was" +
                            " probably exceeded")
            # We force it, sometimes it does not work well...
            if ds < 10:
                time.sleep(1.0)
                return self.get_suggestion(query, lang, ds + 1)
            return None, False
