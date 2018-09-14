import requests
from urllib.parse import quote
import json
import os
from browser_autocomplete_submodule import BrowserAutocompleteSubmodule

headers = {'User-agent':'Mozilla/5.0'}
# baseurl = "http://clients1.google.com/complete/search?"
baseurl = "http://google.com/complete/search?"
cache_dir = "google-cache/"

class SubmoduleGoogleAutocomplete(BrowserAutocompleteSubmodule):
    """SubmoduleGoogleAutocomplete
    A submodule for the google autocomplete triple generation
    """

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Google Autocomplete"
        if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
        self.time_between_queries = 1.0
        self.default_number_suggestions = 10

    def get_suggestion(self, query, lang="en", ds=''):
        """Query Google suggest service"""
        suggestions = []
        # Cache
        fname = cache_dir + query.replace(" ", "-")
        if os.path.isfile(fname):
            with open(fname) as f:
                for line in f:
                    sugg = line.strip().split("\t")
                    suggestions.append((sugg[0], int(sugg[1])))
            return (suggestions, True)
        print(query)
        if query:
            query = quote(query)
            url = baseurl + "hl=%s&q=%s&json=t&ds=%s&client=serp" \
                % (lang, query, ds)
            response = requests.get(url, headers=headers)
            if response.ok:
                result = json.loads(response.content)
                # Append the ranking
                suggestions = [(result[1][i], i) for i in range(len(result[1]))]
            else:
                # Kicked by the search engine
                print("Problem with", query)
                return (None, False)
        # Cache
        with open(fname, "w") as f:
            for sugg in suggestions:
                f.write(str(sugg[0]) + "\t" + str(sugg[1]) + "\n")
        return (suggestions, False)
