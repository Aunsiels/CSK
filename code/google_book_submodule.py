import os
import logging
import time
import re
from bs4 import BeautifulSoup

from apiclient.discovery import build
import inflect

from submodule_interface import SubmoduleInterface

api_key = ""
with open("parameters.tsv") as f:
    for line in f:
        line = line.strip().split("\t")
        if line[0] == "google-book-key":
            api_key = line[1]

service = build('books', 'v1', developerKey=api_key)
plural_engine = inflect.engine()

cache_dir = "googlebook-cache/"
cache_file = cache_dir + "cache.tsv"

calls_per_seconds = 1

class GoogleBookSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Google Book Submodule"
        self._cache = dict()
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        if os.path.isfile(cache_file):
            with open(cache_file) as f:
                for line in f:
                    line = line.strip().split("\t")
                    if len(line) == 2:
                        self._cache[line[0]] = int(line[1])

    def _get_occurences_books(self, q):
        if q in self._cache:
            return self._cache[q]
        req = service.volumes().list(q=q, maxResults=1)
        response = req.execute()
        if match_query(q, response):
            total = response["totalItems"]
        else:
            total = 0
        with open(cache_file, "a") as f:
            f.write(q + "\t" + str(total) + "\n")
        self._cache[q] = total
        time.sleep(1.0 / calls_per_seconds)
        return total


    def _get_query_from_fact(self, fact):
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

    def process(self, input_interface):
        logging.info("Start the verification using google book")
        new_gfs = []
        maxi = 0
        for gf in input_interface.get_generated_facts():
            if gf.get_module_source().get_name() == self._module_reference.get_name():
                continue
            query = self._get_query_from_fact(gf)
            occurences = 0
            try:
                occurences = self._get_occurences_books(query)
            except Exception as e:
                logging.warning(str(e))
                break
            maxi = max(maxi, occurences)
            new_gf = gf.change_score(occurences)\
                       .change_module_source(self._module_reference)\
                       .change_submodule_source(self)\
                       .remove_sentence()
            new_gfs.append(new_gf)
        for i in range(len(new_gfs)):
            new_score = new_gfs[i].get_score() / maxi
            new_gfs[i] = new_gfs[i].change_score(new_score)
        return input_interface.add_generated_facts(new_gfs)


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
