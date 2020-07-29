import unittest

from quasimodo.inflect_accessor import InflectAccessor


class TestIdenticalSubjectObject(unittest.TestCase):

    def setUp(self) -> None:
        self.inflect = InflectAccessor()

    def test_simple_singular(self):
        self.assertEqual(self.inflect.to_singular("apples"), "apple")

    def test_simple_plural(self):
        self.assertEqual(self.inflect.to_plural("apple"), "apples")

    def test_composed_plural(self):
        self.assertEqual(self.inflect.to_plural("red apple"),
                         "red apples")

    def test_oyster(self):
        self.assertEqual(self.inflect.to_plural("perl oyster"),
                         "perl oysters")

    def test_singular_no_transform(self):
        self.assertEqual(self.inflect.to_singular("perl oyster"),
                         "perl oyster")

    def test_mars(self):
        self.assertEqual(self.inflect.to_singular("mars"), "mars")

    def test_jeans(self):
        self.assertEqual(self.inflect.to_singular("jeans"), "jeans")


if __name__ == '__main__':
    unittest.main()
