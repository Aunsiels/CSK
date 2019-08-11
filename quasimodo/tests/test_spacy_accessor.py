import unittest

from quasimodo.spacy_accessor import SpacyAccessor


class TestSpacyAccessor(unittest.TestCase):

    def test_lemmatization(self):
        spacy_accessor = SpacyAccessor()
        self.assertEqual(spacy_accessor.lemmatize("The birds are here"), ["the", "bird", "be", "here"])

    def test_lemmatize_multiple_sentences(self):
        spacy_accessor = SpacyAccessor()
        self.assertEqual(spacy_accessor.lemmatize_multiple(["the birds are here", "the elephants are big"]),
                         [["the", "bird", "be", "here"], ["the", "elephant", "be", "big"]])

    def test_lemmatize_multiple_sentences_two_parts(self):
        spacy_accessor = SpacyAccessor()
        spacy_accessor._nlp.max_length = 30
        self.assertEqual(spacy_accessor.lemmatize_multiple(["the birds are here", "the elephants are big"]),
                         [["the", "bird", "be", "here"], ["the", "elephant", "be", "big"]])

    def test_lemmatize_multiple_sentences_with_ending_tab(self):
        spacy_accessor = SpacyAccessor()
        self.assertEqual(spacy_accessor.lemmatize_multiple(["the birds are here\t", "the elephants are big"]),
                         [["the", "bird", "be", "here", "\t"], ["the", "elephant", "be", "big"]])


if __name__ == '__main__':
    unittest.main()
