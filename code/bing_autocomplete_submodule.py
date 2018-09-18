import requests
from urllib.parse import quote
import http.client, urllib.parse, json
from string import ascii_lowercase
import os
from browser_autocomplete_submodule import BrowserAutocompleteSubmodule
import logging

# Where the cache data are saved
cache_dir = "bing-cache/"
# The subscription key from azure
with open("parameters.tsv") as f:
    for line in f:
        l = line.strip().split("\t")
        if len(l) == 2 and l[0] == "bing-key":
            subscriptionKey = l[1]

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
        self.time_between_queries = 0.02
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
                    suggestions.append((sugg[0], float(sugg[1])))
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
            logging.warning("The number of requests for the bing autocomplete" +
                            " submodule was" +
                            " probably exceeded")
            return (None, False)
