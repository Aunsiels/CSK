import unittest

from quasimodo.sentence_batcher import SentenceBatcher, TooLongBatchException


class TestSentenceBatcher(unittest.TestCase):

    def test_empty(self):
        sb = SentenceBatcher([], 1, len)
        self.assertEqual(len([x for x in sb]), 0)

    def test_one_element(self):
        sb = SentenceBatcher(["The sky is blue"], 30, len)
        batches = [x for x in sb]
        self.assertEqual(len(batches), 1)
        self.assertEqual(batches, [["The sky is blue"]])

    def test_two_elements_in_one_batch(self):
        sentences = ["The sky is blue", "pandas are white"]
        sb = SentenceBatcher(sentences, 100, len)
        batches = [x for x in sb]
        self.assertEqual(batches, [sentences])

    def test_two_elements_in_two_batches(self):
        sentences = ["The sky is blue", "pandas are white"]
        sb = SentenceBatcher(sentences, 20, len)
        batches = [x for x in sb]
        self.assertEqual(batches, [[sentences[0]], [sentences[1]]])

    def test_three_elements_in_two_batches(self):
        sentences = ["The sky is blue", "pandas are white", "the bear is small"]
        sb = SentenceBatcher(sentences, 40, len)
        batches = [x for x in sb]
        self.assertEqual(batches, [sentences[0: 2], sentences[2:3]])

    def test_one_element_too_long(self):
        sentences = ["The sky is blue"]
        sb = SentenceBatcher(sentences, 5, len)
        with self.assertRaises(TooLongBatchException):
            [x for x in sb]


if __name__ == '__main__':
    unittest.main()
