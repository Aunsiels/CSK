from submodule_interface import SubmoduleInterface
import logging
import os
import wikipedia

import spacy

nlp = spacy.load('en_core_web_sm', disable=["tagger", "parser", "ner"])

class WikipediaCooccurrenceSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Wikipedia Cooccurrence"
        self._cache_dir = "wikipedia-cache/"
        self._lang = "en"
        if not os.path.exists(self._cache_dir):
            os.makedirs(self._cache_dir)

    def _get_wikipidia_page_content(self, name):
        fname = self._cache_dir + name.replace(" ", "_")
        content = ""
        if os.path.isfile(fname):
            with open(fname) as f:
                content = f.read().strip()
        else:
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
            with open(fname, "w") as f:
                f.write(content)
        return content

    def process(self, input_interface):
        logging.info("Start the wikipedia cooccurence checking")
        wikipedia.set_lang(self._lang)
        gf = input_interface.get_generated_facts()
        # Groupby subject
        by_subject = dict()
        for g in gf:
            if g.get_module_source().get_name() == self._module_reference.get_name():
                continue
            subj = g.get_subject().get()
            if subj in by_subject:
                by_subject[subj].append(g)
            else:
                by_subject[subj] = [g]

        new_generated_facts = []
        # Retreive page
        for subj in by_subject:
            content = self._get_wikipidia_page_content(subj).lower()
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
                for i in range(len(po)):
                    for j in range(i+1, len(po) + 1):
                        po_temp = " ".join(po[i:j])
                        counter += j-i
                        if po_temp in content:
                            score += j-i
                score /= counter
                if score != 0:
                    new_generated_facts.append(g.change_score(score)
                                               .change_module_source(
                                                   self._module_reference)
                                               .change_submodule_source(
                                                   self).remove_sentence())
        return input_interface.add_generated_facts(new_generated_facts)

def lemmatize(s):
    doc = nlp(s)
    res = []
    for x in doc:
        res.append(x.lemma_)
    return " ".join(res)
