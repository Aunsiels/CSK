from submodule_interface import SubmoduleInterface
import logging
import os
import wikipedia
from nltk.tokenize import word_tokenize


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
            subj = g.get_subject().get()
            if subj in by_subject:
                by_subject[subj].append(g)
            else:
                by_subject[subj] = [g]

        new_generated_facts = []
        # Retreive page
        for subj in by_subject:
            content = self._get_wikipidia_page_content(subj).lower()
            content = word_tokenize(content)
            # TODO: Some preprocessing?
            for g in by_subject[subj]:
                if g.get_object().get().lower() in content:
                    # Better score ?
                    new_score = 0.5
                    if g.get_predicate().get().lower() in content:
                        new_score += 0.5
                    new_generated_facts.append(g.change_score(new_score)
                                               .change_module_source(
                                                   self._module_reference)
                                               .change_submodule_source(
                                                   self))
        return input_interface.add_generated_facts(new_generated_facts)
