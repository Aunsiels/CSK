import logging

import spacy

from quasimodo.submodule_interface import SubmoduleInterface

nlp = spacy.load('en_core_web_sm', disable=["tagger", "parser", "ner"])


def lemmatize_contents(contents):
    for i in range(len(contents)):
        if contents[i] is not None:
            contents[i] = lemmatize(contents[i].lower())


class ContentComparator(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference

    def process(self, input_interface):
        logging.info("Start the wikipedia cooccurrence checking")
        while True:
            try:
                self.setup_processing(input_interface)
                break
            except Exception as e:
                logging.info("Failed to setup the content comparator")
        generated_facts = input_interface.get_generated_facts()
        # Group by subject
        by_subject = self.group_by_subject(generated_facts)

        # Retrieve page
        for subject in by_subject:
            try:
                contents = self.get_contents(subject)
                contents = [x for x in contents if x is not None]
            except Exception as e:
                logging.info("Problem with " + subject + " " + str(e))
                continue
            lemmatize_contents(contents)
            for generated_fact in by_subject[subject]:
                scores = []
                for content in contents:
                    scores.append(self.get_score_generated_fact_given_lemmatized_content(content, generated_fact))
                if scores:
                    generated_fact.get_score().add_score(sum(scores) / len(scores), self._module_reference, self)
        return input_interface

    def get_score_generated_fact_given_lemmatized_content(self, lemmatized_content, generated_fact):
        obj = generated_fact.get_object().get().lower().split(" ")
        pred = generated_fact.get_predicate().get().lower()
        neg = generated_fact.is_negative()
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
        po = lemmatize(pred + " " + " ".join(obj))
        popo = po
        score = 0
        counter = 0
        po = po.split(" ")
        for i in range(len(po)):
            for j in range(i + 1, len(po) + 1):
                po_temp = " ".join(po[i:j])
                counter += j - i
                if po_temp in lemmatized_content:
                    score += j - i
        score /= counter
        return score


    def group_by_subject(self, generated_facts):
        by_subject = dict()
        for g in generated_facts:
            subj = g.get_subject().get().lower()
            if subj in by_subject:
                by_subject[subj].append(g)
            else:
                by_subject[subj] = [g]
        return by_subject

    def setup_processing(self, input_interface):
        raise NotImplementedError

    def get_contents(self, subject):
        raise NotImplementedError


def lemmatize(s):
    doc = nlp(s)
    res = []
    for x in doc:
        res.append(x.lemma_)
    return " ".join(res)
