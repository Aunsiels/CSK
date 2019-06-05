import logging
import gensim.downloader as api
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegressionCV
from sklearn import preprocessing
from sklearn.impute import SimpleImputer

to_keep_columns = ['is negative', "Yahoo Questions",
                   'Google Autocomplete', 'Reddit Questions',
                   'Quora Questions',  'Simple Wikipedia Cooccurrence',
                   'Wikipedia Cooccurrence', 'Image Tag submodule',
                   'Answers.com Questions', 'Flickr', 'Google Book Submodule', 'TBC',
                   "CoreNLP", "OpenIE5", "number sentences"]

use_embeddings = False


class Trainer(object):
    """ We want to score the triples """

    def __init__(self, df_file):
        if use_embeddings:
            self._model = api.load("word2vec-google-news-300")
        self._df = pd.read_csv(df_file, sep="\t", index_col=False)
        self._df = self._df[self._df["label"] != -1]
        self._clf = LogisticRegressionCV(cv=5, max_iter=3000, n_jobs=-1)
        self._filter = [i for i, x in enumerate(self._df.columns)
                        if x in to_keep_columns]
        self._to_keep_columns = [x for x in self._df.columns if x in to_keep_columns]
        self.scaler = preprocessing.StandardScaler()
        self.inputer = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=-1)

    def train(self):
        X = []
        y = []
        logging.info("Preparing data from")
        for i, row in self._df.iterrows():
            spo = self._get_array_generated_fact(row["subject"],
                                                 row["predicate"],
                                                 row["object"])
            x = np.array(row[self._to_keep_columns])
            x = np.concatenate((x, spo))
            X.append(x)
            y.append(row["label"])
        X = np.array(X).astype(np.float64)
        self.inputer.fit(X)
        X = self.inputer.transform(X)
        self.scaler.fit(X)
        X = self.scaler.transform(X)
        y = np.array(y).astype(int)
        logging.info("Random classifier %f", sum(y) / len(y))
        logging.info("Learning model...")
        self._clf.fit(X, y)
        logging.info("Parameters values")
        logging.info("\n".join([str(x[0]) + "\t" + str(x[1]) for x in zip(self._to_keep_columns, self._clf.coef_[0])]))
        logging.info("Accuracy: " + str(self._clf.score(X, y)) + "%")

    def predict(self, fact, features):
        features = np.array(features)
        features[features == ""] = np.nan
        features = features[self._filter]
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
