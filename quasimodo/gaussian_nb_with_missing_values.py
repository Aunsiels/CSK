import math
import numpy as np
import collections


def get_prior(y, y_unique):
    y_counts = collections.Counter(y)
    for key in y_unique:
        y_counts[key] /= y.shape[0]
    return y_counts


def get_means_and_variances(x_input, y, y_unique):
    n_features = x_input.shape[1]
    n_classes = y_unique.shape[0]
    means = np.ones((n_classes, n_features))
    variances = np.ones((n_classes, n_features))
    specific_input = dict()
    for out_class in y_unique:
        specific_input[out_class] = x_input[y == out_class]
    for i in range(n_classes):
        for j in range(n_features):
            temp = specific_input[y_unique[i]][:, j]
            temp = temp[~np.isnan(temp)]
            if temp.shape[0] <= 1:
                means[i, j] = 0
                variances[i, j] = 0
            else:
                means[i, j] = np.mean(temp)
                variances[i, j] = np.var(temp) * (temp.shape[0] / (temp.shape[0] - 1))
    return means, variances


def get_gaussian(x, mean, variance):
    if variance == 0:
        return 1.0
    return 1.0 / math.sqrt(2 * math.pi * variance ** 2) * \
        math.exp(-(x - mean) ** 2 / 2.0 / variance ** 2)


def get_all_likelihoods(x, means, variances):
    result = []
    for i in range(means.shape[0]):
        product = 1.0
        for j in range(means.shape[1]):
            if not np.isnan(x[j]):
                product *= get_gaussian(x[j], means[i, j], variances[i, j])
        result.append(product)
    return np.array(result)


def get_all_posterior(likelihoods, prior):
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
        self.variances = None
        self.prior = None
        self.y_unique = None

    def fit(self, x_input, y):
        self.y_unique = np.unique(y)
        self.prior = get_prior(y, self.y_unique)
        self.means, self.variances = get_means_and_variances(x_input, y, self.y_unique)
        return self

    def predict_proba(self, x_input):
        likelihoods = np.apply_along_axis(lambda x: get_all_likelihoods(x, self.means, self.variances), 1, x_input)
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
