import unittest

from quasimodo.fact import Fact


class TestFact(unittest.TestCase):

    def test_easy(self):
        fact = Fact("elephant", "eat", "herbs")
        self.assertEqual(fact.to_sentence(), "elephants eat herbs")

    def test_has_property(self):
        fact = Fact("elephant", "has_property", "big")
        self.assertEqual(fact.to_sentence(), "elephants are big")

    def test_has_color(self):
        fact = Fact("elephant", "has_color", "grey")
        self.assertEqual(fact.to_sentence(), "elephants are grey")

    def test_body_part(self):
        fact = Fact("elephant", "has_body_part", "ears")
        self.assertEqual(fact.to_sentence(), "elephants have ears")

    def test_some_modality(self):
        fact = Fact("elephant", "has_property", "white", "some[subj/white]")
        self.assertEqual(fact.to_sentence(), "(white) elephants are white")

    def test_always_modality(self):
        fact = Fact("elephant", "has_property", "white", "always")
        self.assertEqual(fact.to_sentence(), "elephants are [always] white")

    def test_negative(self):
        fact = Fact("elephant", "eat", "grass", negative=True)
        self.assertEqual(fact.to_sentence(), "elephants do not eat grass")

    def test_negative_are(self):
        fact = Fact("elephant", "has_property", "small", negative=True)
        self.assertEqual(fact.to_sentence(), "elephants are not small")

    def test_negate_can(self):
        fact = Fact("elephant", "can", "jump", negative=True)
        self.assertEqual(fact.to_sentence(), "elephants cannot jump")

    def test_negate_be(self):
        fact = Fact("elephant", "be in", "europe", negative=True)
        self.assertEqual(fact.to_sentence(), "elephants are not in europe")

    def test_sentence_with_be(self):
        fact = Fact("elephant", "be in", "africa")
        self.assertEqual(fact.to_sentence(), "elephants are in africa")

if __name__ == '__main__':
    unittest.main()
