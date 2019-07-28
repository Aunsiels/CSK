import logging
import gensim.downloader as api
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score

from quasimodo.gaussian_nb_with_missing_values import GaussianNBWithMissingValues

to_keep_columns = ['is negative', "Yahoo Questions",
                   'Google Autocomplete', 'Reddit Questions',
                   'Quora Questions',  'Simple Wikipedia Cooccurrence',
                   'Wikipedia Cooccurrence', 'Image Tag submodule',
                   'Answers.com Questions', 'Flickr', 'Google Book Submodule', 'TBC',
                   "CoreNLP", "OpenIE5", "number sentences", "Conceptual Caption"]

use_embeddings = False


class Trainer(object):
    """ We want to score the triples """

    def __init__(self, df_file):
        if use_embeddings:
            self._model = api.load("word2vec-google-news-300")
        self._df = pd.read_csv(df_file, sep="\t", index_col=False)
        self._clf = GaussianNBWithMissingValues()
        self._filter = [i for i, x in enumerate(self._df.columns)
                        if x in to_keep_columns]
        self._to_keep_columns = [x for x in self._df.columns if x in to_keep_columns]
        for x in self._df.columns:
            if x not in to_keep_columns:
                logging.info(str(x) + " was ignored")
        for x in self._to_keep_columns:
            self._df[x + "_is_nan"] = self._df[x].isna().astype(float)
        self._to_keep_columns += [x + "_is_nan" for x in self._to_keep_columns]
        self._all_df = self._df
        self._df = self._df[self._df["label"] != -1]
        self.scaler = preprocessing.StandardScaler()
        self.inputer = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=np.nan)

    def train(self):
        x_input = []
        y = []
        logging.info("Preparing data from")
        for i, row in self._df.iterrows():
            spo = self._get_array_generated_fact(row["subject"],
                                                 row["predicate"],
                                                 row["object"])
            x = np.array(row[self._to_keep_columns])
            x = np.concatenate((x, spo))
            x_input.append(x)
            y.append(row["label"])
        x_input = np.array(x_input).astype(np.float64)
        self.inputer.fit(x_input)
        x_input = self.inputer.transform(x_input)
        self.scaler.fit(x_input)
        x_input = self.scaler.transform(x_input)
        y = np.array(y).astype(int)
        logging.info("Random classifier %0.2f", sum(y) / len(y))
        logging.info("Learning model...")
        scores = cross_val_score(self._clf, x_input, y, cv=5)
        self._clf.fit(x_input, y)
        logging.info("Cross validation Accuracy: %0.2f (+/- %0.2f)", scores.mean(), scores.std() * 2)
        logging.info("Accuracy on original data: %0.2f", self._clf.score(x_input, y))

    def predict(self, fact, features):
        features = np.array(features)
        features[features == ""] = np.nan
        features = features[self._filter]
        features = np.concatenate((features, np.isnan(features).astype(float)))
        features = features.astype(np.float64)
        spo = self._get_array_generated_fact(fact.get_subject().get(),
                                             fact.get_predicate().get(),
                                             fact.get_object().get())
        features = np.concatenate((features, spo))
        features = self.inputer.transform([features])
        features = self.scaler.transform(features)
        return self._clf.predict_proba(features)[0][1]

    def _get_array(self, sentence):
        if not use_embeddings:
            return np.array([])
        sentence = sentence.lower().replace("_", " ")
        sentence = word_tokenize(sentence)
        res = np.zeros(self._model.vector_size)
        counter = 0
        for word in sentence:
            if word in self._model.vocab:
                res += self._model.get_vector(word)
                counter += 1
        if counter == 0:
            return res
        else:
            return res / counter

    def _get_array_generated_fact(self, subj, pred, obj):
        subj = self._get_array(subj)
        pred = self._get_array(pred)
        obj = self._get_array(obj)
        return np.concatenate([subj, pred, obj])
