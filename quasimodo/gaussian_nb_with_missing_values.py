import math
import numpy as np
import collections


class GaussianNBWithMissingValues:

    def __init__(self, epsilon=1e-4):
        self.epsilon = epsilon
        self.means = None
        self.standard_deviations = None
        self.prior = None
        self.y_unique = None
        self.values = None

    def fit(self, x_input, y):
        if x_input is None or y is None:
            return self
        self.set_unique_y(y)
        self.set_prior(y)
        self.set_means_and_standard_deviations(x_input, y)
        self.set_values(x_input, y, self.y_unique)
        return self

    def set_unique_y(self, y):
        self.y_unique = np.unique(y)  # This is sorted

    def predict_proba(self, x_input):
        likelihoods = np.apply_along_axis(
            lambda x: self.get_all_likelihoods(x), 1, x_input)
        probabilities = np.apply_along_axis(lambda x: self.get_all_posterior(x), 1, likelihoods)
        return probabilities

    def predict(self, x_input):
        probabilities = self.predict_proba(x_input)
        indexes = np.argmax(probabilities, axis=1)
        res = []
        for index in indexes:
            res.append(self.y_unique[index])
        return np.array(res)

    def set_values(self, x_input, y, y_unique):
        n_features = x_input.shape[1]
        n_classes = y_unique.shape[0]
        reversed_label = dict()
        for i, label in enumerate(y_unique):
            reversed_label[label] = i
        self.values = [[dict() for _ in range(n_features)] for _ in range(n_classes)]
        for idx, row in enumerate(x_input):
            j = reversed_label[y[idx]]
            for i, value in enumerate(row):
                if np.isnan(value):
                    continue
                if len(self.values[j][i]) <= 3:
                    self.values[j][i][value] = self.values[j][i].get(value, 0) + 1

    def get_all_posterior(self, likelihoods):
        if self.prior is None:
            return [1 / likelihoods.shape[0]] * likelihoods.shape[0]
        res = []
        for i, likelihood in enumerate(likelihoods):
            temp = likelihood + math.log(self.prior[i])
            res.append(temp)
        res = np.array(res)
        max_res = res.max()
        normalization_term = max_res + np.log(np.exp(res - max_res).sum())
        res -= normalization_term
        res = np.exp(res)
        return res

    def get_all_likelihoods(self, x):
        if self.means is None or self.standard_deviations is None:
            if x is not None:
                return [1 / x.shape[0]] * x.shape[0]
            else:
                return []
        result = []
        for i in range(self.means.shape[0]):
            product = 0.0
            for j in range(self.means.shape[1]):
                if not np.isnan(x[j]):
                    if self.values is not None and len(self.values[i][j]) == 0:
                        temp = 0.0
                    elif self.values is not None and len(self.values[i][j]) == 1:
                        if x[j] in self.values[i][j]:
                            temp = 1.0
                        else:
                            temp = 0.0
                    elif self.values is not None and len(self.values[i][j]) == 2:
                        if x[j] in self.values[i][j]:
                            temp = self.values[i][j][x[j]] / sum(self.values[i][j].values())
                        else:
                            temp = 0.0
                    else:
                        temp = self.get_gaussian(x[j], self.means[i, j], self.standard_deviations[i, j])
                    # We do not want zero probabilities
                    temp = min(1.0, temp + self.epsilon)
                    product += math.log(temp)
            result.append(product)
        return np.array(result)

    def get_gaussian(self, x, mean, standard_deviation):
        if abs(standard_deviation) < self.epsilon:
            if abs(x - mean) < self.epsilon:
                return 1.0
            else:
                return 0.0
        return 1.0 / math.sqrt(2 * math.pi * standard_deviation ** 2) * \
            math.exp(-(x - mean) ** 2 / 2.0 / standard_deviation ** 2)

    def set_prior(self, y):
        self.prior = collections.Counter(y)
        for key in self.y_unique:
            self.prior[key] /= y.shape[0]
        return self.prior

    def set_means_and_standard_deviations(self, x_input, y):
        n_features = x_input.shape[1]
        n_classes = self.y_unique.shape[0]
        self.means = np.ones((n_classes, n_features))
        self.standard_deviations = np.ones((n_classes, n_features))
        specific_input = dict()
        for out_class in self.y_unique:
            specific_input[out_class] = x_input[y == out_class]
        for i in range(n_classes):
            for j in range(n_features):
                temp = specific_input[self.y_unique[i]][:, j]
                temp = temp[~np.isnan(temp)]
                if temp.shape[0] <= 1:
                    self.means[i, j] = 0
                    self.standard_deviations[i, j] = 0
                else:
                    self.means[i, j] = np.mean(temp)
                    self.standard_deviations[i, j] = np.std(temp, ddof=1)

    def score(self, x_input, y):
        predictions = self.predict(x_input)
        return sum(predictions == y) / y.shape[0]

    def get_params(self, deep=True):
        return {}

    def set_params(self, params):
        pass
