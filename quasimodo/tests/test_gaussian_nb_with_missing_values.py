import unittest

import numpy as np

from quasimodo.assertion_fusion.gaussian_nb_with_missing_values import GaussianNBWithMissingValues


class TestFilterObject(unittest.TestCase):

    def test_gaussian2(self):
        std = -0.1339048038303071
        mean = -0.1339048038303071
        x = 150.10086283379565
        temp = self.gaussian_nb.get_gaussian(x, mean, std)
        self.assertAlmostEqual(temp, 0)

    def test_prior(self):
        y = np.array([1] * 10 + [0] * 5)
        self.gaussian_nb.set_unique_y(y)
        self.gaussian_nb.set_prior(y)
        prior = self.gaussian_nb.prior
        self.assertAlmostEqual(prior[0], 0.33, places=2)
        self.assertAlmostEqual(prior[1], 0.67, places=2)

    def test_means_standard_deviations(self):
        x = [[0, 0],
             [0, 0],
             [1, -1],
             [1, 0],
             [1, 0],
             [2, 3]]
        y = [0, 0, 0, 1, 1, 1]
        x = np.array(x)
        y = np.array(y)
        self.gaussian_nb.fit(x, y)
        means = self.gaussian_nb.means
        standard_deviations = self.gaussian_nb.standard_deviations
        self.assertAlmostEqual(means[0, 0], 0.33, places=2)
        self.assertAlmostEqual(means[0, 1], -0.33, places=2)
        self.assertAlmostEqual(means[1, 0], 1.33, places=2)
        self.assertAlmostEqual(means[1, 1], 1, places=2)
        self.assertAlmostEqual(standard_deviations[0, 0] ** 2, 0.33, places=2)
        self.assertAlmostEqual(standard_deviations[0, 1] ** 2, 0.33, places=2)
        self.assertAlmostEqual(standard_deviations[1, 0] ** 2, 0.33, places=2)
        self.assertAlmostEqual(standard_deviations[1, 1] ** 2, 3, places=2)

    def test_means_standard_deviations_with_nan(self):
        self.gaussian_nb.fit(self.x, self.y)
        means = self.gaussian_nb.means
        standard_deviations = self.gaussian_nb.standard_deviations
        self.assertAlmostEqual(means[0, 0], 0.33, places=2)
        self.assertAlmostEqual(means[0, 1], -0.33, places=2)
        self.assertAlmostEqual(means[1, 0], 1.33, places=2)
        self.assertAlmostEqual(means[1, 1], 1, places=2)
        self.assertAlmostEqual(standard_deviations[0, 0] ** 2, 0.33, places=2)
        self.assertAlmostEqual(standard_deviations[0, 1] ** 2, 0.33, places=2)
        self.assertAlmostEqual(standard_deviations[1, 0] ** 2, 0.33, places=2)
        self.assertAlmostEqual(standard_deviations[1, 1] ** 2, 3, places=2)

    def test_likelihoods(self):
        self.gaussian_nb.fit(self.x, self.y)
        x_in = np.array([1, 0])
        likelihoods = self.gaussian_nb.get_all_likelihoods(x_in)
        self.assertNotAlmostEqual(likelihoods[0], 0, places=2)
        self.assertNotAlmostEqual(likelihoods[0], 1, places=2)
        self.assertNotAlmostEqual(likelihoods[1], 0, places=2)
        self.assertNotAlmostEqual(likelihoods[1], 1, places=2)

    def setUp(self):
        self.x = [[0, np.nan],  # 0
                  [np.nan, 0],  # 0
                  [0, 0],  # 0
                  [1, -1],  # 0
                  [1, np.nan],  # 1
                  [np.nan, 0],  # 1
                  [1, 0],  # 1
                  [2, 3]]  # 1
        self.y = [0, 0, 0, 0, 1, 1, 1, 1]
        self.y_uniq = [0, 1]
        self.x = np.array(self.x)
        self.y = np.array(self.y)
        self.y_uniq = np.array(self.y_uniq)
        self.gaussian_nb = GaussianNBWithMissingValues()

    def test_predict_proba(self):
        clf = GaussianNBWithMissingValues()
        clf.fit(self.x, self.y)
        x_in = np.array([[1, 0]])
        proba = clf.predict_proba(x_in)
        self.assertNotAlmostEqual(proba[0][0], 0, places=2)
        self.assertNotAlmostEqual(proba[0][0], 1, places=2)
        self.assertNotAlmostEqual(proba[0][1], 0, places=2)
        self.assertNotAlmostEqual(proba[0][1], 1, places=2)
        self.assertGreater(proba[0][1], proba[0][0])

    def test_gaussian(self):
        gaussian = self.gaussian_nb.get_gaussian(0.441, 1, 0.447213595)
        self.assertAlmostEqual(gaussian, 0.40842, places=2)


if __name__ == '__main__':
    unittest.main()