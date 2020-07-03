import logging
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import AdaBoostClassifier
from sklearn.impute import SimpleImputer
import gensim.downloader as api
from sklearn.linear_model import LogisticRegressionCV

from quasimodo.assertion_fusion.gaussian_nb_with_missing_values import GaussianNBWithMissingValues
from quasimodo.assertion_output.closest_indexes import ClosestIndexes

to_keep_columns = ['is negative', "Yahoo Questions",
                   'Google Autocomplete', 'Reddit Questions',
                   'Quora Questions', 'Simple Wikipedia Cooccurrence',
                   'Wikipedia Cooccurrence', 'Image Tag submodule',
                   'Answers.com Questions', 'Flickr', 'Google Book Submodule',
                   'TBC',
                   "CoreNLP", "OpenIE5", "Manual", "number sentences",
                   "Conceptual Caption",
                   "What questions file", "number modalities"]

SLICE_SIZE = 10000  # Change this in case of Memory problems

use_embeddings = False


class Trainer(object):
    """ We want to score the triples """

    def __init__(self, df_file):
        self._model = api.load(
            "glove-wiki-gigaword-50")
        self._df = pd.read_csv(df_file, sep="\t", index_col=False)
        # self._clf = GaussianNBWithMissingValues()
        # self._clf = AdaBoostClassifier(n_estimators=200)
        self._clf = LogisticRegressionCV(max_iter=5000, n_jobs=-1)
        self._filter = [i for i, x in enumerate(self._df.columns)
                        if x in to_keep_columns]
        self._to_keep_columns = [x for x in self._df.columns if
                                 x in to_keep_columns]

        # Feature creation
        for x in self._df.columns:
            if x not in to_keep_columns:
                logging.info(str(x) + " was ignored")
        for x in self._to_keep_columns:
            self._df[x + "_is_nan"] = self._df[x].isna().astype(float)
        self._to_keep_columns += [x + "_is_nan" for x in self._to_keep_columns]
        self.create_patterns_features()
        # self.set_closest_features()

        # End
        self._all_df = self._df
        self.scaler = preprocessing.StandardScaler()
        self.scaler.fit(self._all_df[self._to_keep_columns])
        self._df = self._df[self._df["label"] != -1]
        logging.info(str(len(self._df)) + " annotated facts given.")
        self.inputer = SimpleImputer(missing_values=np.nan,
                                     strategy='constant', fill_value=0.0)

    def set_closest_features(self):
        vectors = self.get_vectors()
        closest_indexes_compute = ClosestIndexes(vectors)
        closest_indexes = closest_indexes_compute.get_closest_indexes(
            2, SLICE_SIZE)
        for column in self._to_keep_columns:
            if column in self._df.columns:
                self._df[column + "-closest"] = np.zeros(len(self._df))
        closest_columns = [column + "-closest"
                           for column in self._to_keep_columns
                           if column in self._df.columns]
        for i, row in self._df.iterrows():
            to_copy = self._df.iloc[closest_indexes[i][1][0]]
            self._df.loc[i, closest_columns] = [
                to_copy[column] * closest_indexes[i][1][1]
                for column in self._to_keep_columns
                if column in self._df.columns
            ]
        self._to_keep_columns += closest_columns

    def get_vectors(self):
        vector = np.zeros((len(self._df),
                           self._model.vector_size * 3),
                          dtype=float)
        for i, row in self._df.iterrows():
            vector[i, :] = self._get_array_generated_fact(
                row.subject,
                row.predicate,
                row.object
            )
        return vector

    def get_all_patterns(self):
        patterns = set()
        for string_patterns in self._df["patterns"]:
            for pattern in get_patterns(string_patterns):
                patterns.add(pattern)
        return patterns

    def add_patterns_to_df(self):
        size = len(self._df)
        for pattern in self.patterns:
            self._df[pattern] = np.zeros(size)
        for i, string_patterns in enumerate(self._df["patterns"]):
            for pattern in get_patterns(string_patterns):
                self._df[pattern].iloc[i] += 1

    def get_pattern_row(self, pattern):
        pattern_features = np.zeros(len(self.patterns))
        row_patterns = get_patterns(pattern)
        for pattern in row_patterns:
            if pattern in self.patterns:
                pattern_features[self.patterns.index(pattern)] += 1
        return pattern_features

    def create_patterns_features(self):
        self.patterns = list(self.get_all_patterns())
        self.patterns_index = \
        [i for i, x in enumerate(self._df.columns) if x == "patterns"][0]
        self.add_patterns_to_df()
        self._to_keep_columns += self.patterns

    def train(self):
        x_input = []
        y = []
        logging.info("Preparing data from")
        for i, row in self._df.iterrows():
            x = np.array(row[self._to_keep_columns])
            x_input.append(x)
            y.append(row["label"])
        x_input = np.array(x_input).astype(np.float64)
        self.inputer.fit(x_input)
        x_input = self.inputer.transform(x_input)
        x_input = self.scaler.transform(x_input)
        y = np.array(y).astype(int)
        logging.info("Random classifier %0.2f", sum(y) / len(y))
        logging.info("Learning model...")
        from imblearn.over_sampling import SMOTE
        smote = SMOTE()
        x_input, y = smote.fit_resample(x_input, y)
        self._clf.fit(x_input, y)
        logging.info("Accuracy on original data: %0.2f",
                     self._clf.score(x_input, y))
        # logging.info("Parameters:")
        # logging.info("Priors:")
        # logging.info("0: " + str(self._clf.prior[0]))
        # logging.info("1: " + str(self._clf.prior[1]))
        # logging.info("Means:")
        # for i, column_name in enumerate(self._to_keep_columns):
        #     logging.info(
        #         column_name + ", for 0: " + str(self._clf.means[0][i]) +
        #         ", for 1: " + str(self._clf.means[1][i]))
        # logging.info("Standard deviations:")
        # for i, column_name in enumerate(self._to_keep_columns):
        #     logging.info(column_name + ", for 0: " + str(
        #         self._clf.standard_deviations[0][i]) +
        #                  ", for 1: " + str(
        #         self._clf.standard_deviations[1][i]))

    def predict(self, fact, features):
        features = np.array(features)
        pattern = features[self.patterns_index]
        features[features == ""] = np.nan
        features = features[self._filter].astype(float)
        features = np.concatenate((features, np.isnan(features).astype(float)))
        features = features.astype(np.float64)
        features = np.concatenate(
            (features, self.get_pattern_row(pattern).astype(float)))
        features = self.scaler.transform([features])
        features = self.inputer.transform(features)
        # 0 because only one point
        # 1 because positive is one
        return self._clf.predict_proba(features)[0][1]

    def _get_array(self, sentence):
        sentence = str(sentence).lower().replace("_", " ")
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


def get_patterns(string_patterns):
    if type(string_patterns) == float:
        return []
    return string_patterns.split("; ")
