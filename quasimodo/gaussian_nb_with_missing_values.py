import math
import numpy as np
import collections


def get_prior(y, y_unique):
    y_counts = collections.Counter(y)
    for key in y_unique:
        y_counts[key] /= y.shape[0]
    return y_counts


def get_means_and_standard_deviations(x_input, y, y_unique):
    n_features = x_input.shape[1]
    n_classes = y_unique.shape[0]
    means = np.ones((n_classes, n_features))
    standard_deviations = np.ones((n_classes, n_features))
    specific_input = dict()
    for out_class in y_unique:
        specific_input[out_class] = x_input[y == out_class]
    for i in range(n_classes):
        for j in range(n_features):
            temp = specific_input[y_unique[i]][:, j]
            temp = temp[~np.isnan(temp)]
            if temp.shape[0] <= 1:
                means[i, j] = 0
                standard_deviations[i, j] = 0
            else:
                means[i, j] = np.mean(temp)
                standard_deviations[i, j] = np.std(temp, ddof=1)
    return means, standard_deviations


def get_gaussian(x, mean, standard_deviation):
    if standard_deviation == 0:
        return float(x == mean)
    return 1.0 / math.sqrt(2 * math.pi * standard_deviation ** 2) * \
        math.exp(-(x - mean) ** 2 / 2.0 / standard_deviation ** 2)


def get_all_likelihoods(x, means, standard_deviations):
    if means is None or standard_deviations is None:
        if x is not None:
            return [1 / x.shape[0]] * x.shape[0]
        else:
            return []
    result = []
    for i in range(means.shape[0]):
        product = 1.0
        for j in range(means.shape[1]):
            if not np.isnan(x[j]):
                product *= get_gaussian(x[j], means[i, j], standard_deviations[i, j])
        result.append(product)
    return np.array(result)


def get_all_posterior(likelihoods, prior):
    if prior is None:
        return [1 / likelihoods.shape[0]] * likelihoods.shape[0]
    total = 0
    res = []
    for i, likelihood in enumerate(likelihoods):
        temp = likelihood * prior[i]
        res.append(temp)
        total += temp
    res = np.array(res)
    if total != 0:
        res /= total
    return res


class GaussianNBWithMissingValues:

    def __init__(self):
        self.means = None
        self.standard_deviations = None
        self.prior = None
        self.y_unique = None

    def fit(self, x_input, y):
        if x_input is None or y is None:
            return self
        self.y_unique = np.unique(y)
        self.prior = get_prior(y, self.y_unique)
        self.means, self.standard_deviations = get_means_and_standard_deviations(x_input, y, self.y_unique)
        return self

    def predict_proba(self, x_input):
        likelihoods = np.apply_along_axis(lambda x: get_all_likelihoods(x, self.means, self.standard_deviations), 1, x_input)
        probabilities = np.apply_along_axis(lambda x: get_all_posterior(x, self.prior), 1, likelihoods)
        return probabilities

    def predict(self, x_input):
        probabilities = self.predict_proba(x_input)
        indexes = np.argmax(probabilities, axis=1)
        res = []
        for index in indexes:
            res.append(self.y_unique[index])
        return np.array(res)

    def score(self, x_input, y):
        predictions = self.predict(x_input)
        return sum(predictions == y) / y.shape[0]

    def get_params(self, deep=True):
        return {}

    def set_params(self, params):
        pass
