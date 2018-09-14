import requests
from urllib.parse import quote
import http.client, urllib.parse, json
from string import ascii_lowercase
import os
from browser_autocomplete_submodule import BrowserAutocompleteSubmodule

# Where the cache data are saved
cache_dir = "bing-cache/"
# The subscription key from azure
subscriptionKey = "0eb22ae227ff4a84a6c4d8c38eb9a965"

# Location of the api
host = 'api.cognitive.microsoft.com'
path = '/bing/v7.0/suggestions'

# language
mkt = 'en-US'

class BingAutocompleteSubmodule(BrowserAutocompleteSubmodule):
    """BingAutocompleteSubmodule
    Submodule which generetes assertions using the autocomplete from Bing
    """

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Bing Autocomplete"
        if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
        self.time_between_queries = 1.0
        self.default_number_suggestions = 8

    def get_suggestion(self, query, lang="en-US", ds=''):
        "Gets Autosuggest results for a query and returns the information."
        suggestions = []
        fname = cache_dir + query.replace(" ", "-")
        # check if the query was done before
        if os.path.isfile(fname):
            with open(fname) as f:
                for line in f:
                    sugg = line.strip().split("\t")
                    suggestions.append((sugg[0], int(sugg[1])))
            return (suggestions, True)

        params = '?mkt=' + lang + '&q=' + quote(query)
        headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", path + params, None, headers)
        response = conn.getresponse()
        # if the response is ok
        if response.status == 200:
            res_json = json.loads(response.read())
            s_temp = []
            for grp in res_json.setdefault("suggestionGroups", []):
                suggs = grp.setdefault("searchSuggestions", [])
                for suggestion in suggs:
                    s_temp.append(suggestion.setdefault("query", ""))
            suggestions = [(s_temp[i], i) for i in range(len(s_temp))]
            # save the result
            with open(fname, "w") as f:
                for sugg in suggestions:
                    f.write(str(sugg[0]) + "\t" + str(sugg[1]) + "\n")
            return (suggestions, False)
        else:
            # We surely exceded the number of requests
            return (None, False)
