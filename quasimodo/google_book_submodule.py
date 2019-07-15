import os
import logging
import time
import re
from bs4 import BeautifulSoup

import apiclient
import inflect

from quasimodo.mongodb_cache import MongoDBCache
from quasimodo.parameters_reader import ParametersReader
from .submodule_interface import SubmoduleInterface

parameters_reader = ParametersReader()
api_key = parameters_reader.get_parameter("google-book-key") or ""
DEFAULT_MONGODB_LOCATION = parameters_reader.get_parameter("default-mongodb-location") or "mongodb://localhost:27017/"

try:
    service = apiclient.discovery.build('books', 'v1', developerKey=api_key)
except:
    service = None

plural_engine = inflect.engine()

cache_dir = os.path.dirname(__file__) + "/googlebook-cache/"
cache_file = cache_dir + "cache.tsv"

calls_per_seconds = 1


class GoogleBookSubmodule(SubmoduleInterface):

    def __init__(self, module_reference, use_cache=True, cache_name="google-book-cache"):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Google Book Submodule"
        self.use_cache = use_cache
        self.cache = MongoDBCache(cache_name, mongodb_location=DEFAULT_MONGODB_LOCATION)

    def _setup_cache(self):
        self._cache = dict()
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        if os.path.isfile(cache_file):
            with open(cache_file) as f:
                for line in f:
                    line = line.strip().split("\t")
                    if len(line) == 2:
                        self._cache[line[0]] = int(line[1])

    def read_cache(self, query):
        if self.use_cache:
            cache_value = self.cache.read_cache(query)
            if cache_value is not None:
                return float(cache_value[0])
        return None

    def write_cache(self, query, total):
        if self.use_cache:
            self.cache.write_cache(query, total)

    def _get_occurrences_books(self, query, only_cache):
        cache_value = self.read_cache(query)
        if cache_value is not None:
            return cache_value
        if only_cache or service is None:
            return -1
        req = service.volumes().list(q=query, maxResults=1)
        response = req.execute()
        if match_query(query, response):
            total = response["totalItems"]
        else:
            total = 0
        self.write_cache(query, total)
        time.sleep(1.0 / calls_per_seconds)
        return total

    def process(self, input_interface):
        logging.info("Start the verification using google book")
        if service is None:
            logging.info("No service found for Google Book")
        maxi = 0
        only_cache = False
        for generated_fact in input_interface.get_generated_facts():
            query = _get_query_from_fact(generated_fact)
            occurrences = -1
            try:
                occurrences = self._get_occurrences_books(query, only_cache)
            except Exception as e:
                logging.warning(str(e))
                only_cache = True
            maxi = max(maxi, occurrences)
        if maxi == 0:
            maxi = 1
        for generated_fact in input_interface.get_generated_facts():
            query = _get_query_from_fact(generated_fact)
            try:
                occurrences = self._get_occurrences_books(query, only_cache)
            except Exception as e:
                logging.warning(str(e))
                break
            if occurrences != -1:
                generated_fact.get_score().add_score(occurrences / maxi, self._module_reference, self)
        return input_interface


def to_singular_plural(pred):
    pred_l = pred.split(" ")
    pred_res = []
    for word in pred_l:
        if word == "be":
            pred_res.append("are OR is")
        elif word == "have":
            pred_res.append("have OR has")
        else:
            if len(word) <= 2:
                pred_res.append(word)
                continue
            sing = plural_engine.singular_noun(word)
            if not sing:
                pred_res.append(word + " OR " + plural_engine.plural(word))
            else:
                pred_res.append(word + " OR " + sing + " OR " + plural_engine.plural(word))
    return " ".join(pred_res)


def query_to_regex(q):
    q = re.sub('[^a-zA-Z\s]', "", q).split(" ")
    temp = []
    in_or = False
    for i in range(len(q)):
        w = q[i]
        if w == "OR":
            temp.append("|")
        else:
            if i != len(q) - 1 and q[i+1] == "OR" and not in_or:
                temp.append("(")
                in_or = True
            temp.append(w)
            if i != 0 and q[i-1] == "OR":
                if i >= len(q) - 1 or q[i+1] != "OR":
                    temp.append(")")
                    in_or = False
    return re.compile("".join(temp))


def match_query(q, response):
    regex = query_to_regex(q)
    if "items" in response:
        items = response["items"]
    else:
        return False
    if len(items) == 0:
        return False
    item = items[0]
    if "searchInfo" not in item:
        return False
    si = item["searchInfo"]
    if "textSnippet" not in si:
        return False
    text = BeautifulSoup(si["textSnippet"]).get_text().replace("\n", " ").lower()
    text = re.sub("[^a-zA-Z]", "", text)
    return regex.search(text) is not None


def _get_query_from_fact(fact):
    subj = fact.get_subject().get()
    pred = fact.get_predicate().get()
    obj = fact.get_object().get()
    neg = fact.is_negative()
    if pred.startswith("has_") or pred == "hasProperty":
        pred = "are OR is"
        if neg:
            pred += " not"
    else:
        if neg:
            pred_l = pred.split(" ")
            if pred_l[0] == "can":
                pred = "cannot OR can't"
                if len(pred_l) > 1:
                    pred += " " + to_singular_plural(" ".join(pred_l[1:]))
            else:
                pred = "do OR does not " + to_singular_plural(pred)
        else:
            pred = to_singular_plural(pred)
    subj_plur = plural_engine.plural(subj)
    q = '"' + subj + " OR " + subj_plur + " " + pred + " " + \
        to_singular_plural(obj) + '"'
    return q
