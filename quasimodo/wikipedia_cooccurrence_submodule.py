from quasimodo.mongodb_cache import MongoDBCache
from quasimodo.parameters_reader import ParametersReader
from .submodule_interface import SubmoduleInterface
import logging
import wikipedia

import spacy

nlp = spacy.load('en_core_web_sm', disable=["tagger", "parser", "ner"])

parameters_reader = ParametersReader()
DEFAULT_MONGODB_LOCATION = parameters_reader.get_parameter("default-mongodb-location") or "mongodb://localhost:27017/"


class WikipediaCooccurrenceSubmodule(SubmoduleInterface):

    def __init__(self, module_reference, use_cache=True, cache_name="wikipedia-cache"):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Wikipedia Cooccurrence"
        self.use_cache = use_cache
        self._lang = "en"
        self.cache = MongoDBCache(cache_name, mongodb_location=DEFAULT_MONGODB_LOCATION)

    def _get_wikipidia_page_content(self, name):
        content = self.read_cache(name)
        if content is not None:
            return content
        search = wikipedia.search(name)
        # For now, we only consider the first result
        if search:
            try:
                content = wikipedia.page(search[0]).content
            except wikipedia.DisambiguationError as e:
                # Not clear how often it happens
                if e.options:
                    try:
                        content = wikipedia.page(e.options[0]).content
                    except wikipedia.DisambiguationError as e2:
                        if e2.options:
                            temp = e2.options[0].replace("(", "")\
                                .replace(")", "")
                            try:
                                content = wikipedia.page(temp).content
                            except wikipedia.DisambiguationError as e3:
                                pass
                            except wikipedia.exceptions.PageError:
                                logging.warning("Wikipedia page not found: " + name)
                    except wikipedia.exceptions.PageError:
                        logging.warning("Wikipedia page not found: " + name)
            except wikipedia.exceptions.PageError:
                logging.warning("Wikipedia page not found: " + name)
        self.write_cache(name, content)
        return content

    def write_cache(self, wikipedia_page, content):
        if self.use_cache:
            filename = wikipedia_page.replace(" ", "_").replace("/", "_")
            self.cache.write_cache(filename, content)

    def read_cache(self, wikipedia_page):
        if self.use_cache:
            filename = wikipedia_page.replace(" ", "_").replace("/", "_")
            cache_value = self.cache.read_cache(filename)
            if cache_value is not None:
                return cache_value[0]
        return None

    def process(self, input_interface):
        logging.info("Start the wikipedia cooccurence checking")
        wikipedia.set_lang(self._lang)
        gf = input_interface.get_generated_facts()
        # Groupby subject
        by_subject = dict()
        for g in gf:
            subj = g.get_subject().get().lower()
            if subj in by_subject:
                by_subject[subj].append(g)
            else:
                by_subject[subj] = [g]

        # Retreive page
        for subj in by_subject:
            try:
                content = self._get_wikipidia_page_content(subj).lower()
            except:
                logging.info("Problem with " + subj)
                continue
            content = lemmatize(content)
            # TODO: Some preprocessing?
            for g in by_subject[subj]:
                obj = g.get_object().get().lower().split(" ")
                pred = g.get_predicate().get().lower()
                neg = g.is_negative()
                if pred.startswith("has_") or pred == "hasProperty":
                    pred = "are"
                    if neg:
                        pred += " not"
                else:
                    if neg:
                        pred_l = pred.split(" ")
                        if pred_l[0] == "can":
                            pred = "cannot"
                            if len(pred_l) > 1:
                                pred += " " + " ".join(pred_l[1:])
                        else:
                            pred = "do not " + pred
                po = lemmatize(pred + " ".join(obj))
                score = 0
                counter = 0
                po = po.split(" ")
                for i in range(len(po)):
                    for j in range(i+1, len(po) + 1):
                        po_temp = " ".join(po[i:j])
                        counter += j-i
                        if po_temp in content:
                            score += j-i
                score /= counter
                if score != 0:
                    g.get_score().add_score(score, self._module_reference, self)
        return input_interface


def lemmatize(s):
    doc = nlp(s)
    res = []
    for x in doc:
        res.append(x.lemma_)
    return " ".join(res)
