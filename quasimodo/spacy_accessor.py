import spacy

from quasimodo.sentence_batcher import SentenceBatcher

SEPARATOR = "\n\n"
LEN_SEPARATOR = len(SEPARATOR)


class SpacyAccessor(object):

    def __init__(self, model="en_core_web_sm"):
        self._nlp = spacy.load(model)

    def lemmatize(self, sentence):
        tokens = self._nlp(sentence)
        return [x.lemma_ for x in tokens]

    def lemmatize_multiple(self, sentences):
        sb = SentenceBatcher(sentences, self._nlp.max_length, lambda x: len(x) + LEN_SEPARATOR)
        batch_lemmatization = [self.lemmatize(SEPARATOR.join(x)) for x in sb]
        lemmatized_sentences = []
        for batch in batch_lemmatization:
            lemmatized_sentences.append([])
            for lemma in batch:
                if lemma == SEPARATOR:
                    lemmatized_sentences.append([])
                elif SEPARATOR in lemma:
                    lemma_parts = lemma.split(SEPARATOR)
                    for i, part in enumerate(lemma_parts):
                        if len(part) > 0:
                            lemmatized_sentences[-1].append(part)
                        if i != len(lemma_parts) - 1:
                            lemmatized_sentences.append([])
                else:
                    lemmatized_sentences[-1].append(lemma)
        return lemmatized_sentences

    def annotate(self, sentence):
        return self._nlp(sentence)


spacy_annotator = None


def get_default_annotator():
    global spacy_annotator
    if spacy_annotator is None:
        spacy_annotator = SpacyAccessor()
    return spacy_annotator
