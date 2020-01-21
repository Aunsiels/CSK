import unittest

from quasimodo.cache.cachable_querying_system import get_regex_from_query_by_subject, to_filename, \
    get_regex_from_query_by_pattern


def transform_text_subject(text):
    filename = to_filename(text)
    regex = get_regex_from_query_by_subject(filename)
    return regex


def transform_text_pattern(text):
    filename = to_filename(text)
    regex = get_regex_from_query_by_pattern(filename)
    return regex


class TestQueryToRegex(unittest.TestCase):

    def test_subject_0(self):
        regex = transform_text_subject("why are elephants")
        self.assertEqual("elephant", regex)

    def test_subject_1(self):
        regex = transform_text_subject("why can elephants")
        self.assertEqual("elephant", regex)

    def test_subject_2(self):
        regex = transform_text_subject("why is elephant")
        self.assertEqual("elephant", regex)

    def test_subject_3(self):
        regex = transform_text_subject("why can't elephants")
        self.assertEqual("elephant", regex)

    def test_subject_4(self):
        regex = transform_text_subject("why do elephants")
        self.assertEqual("elephant", regex)

    def test_subject_5(self):
        regex = transform_text_subject("why does elephant")
        self.assertEqual("elephant", regex)

    def test_subject_6(self):
        regex = transform_text_subject("how does elephant")
        self.assertEqual("elephant", regex)

    def test_subject_7(self):
        regex = transform_text_subject("why elephant")
        self.assertEqual("elephant", regex)

    def test_subject_8(self):
        regex = transform_text_subject("why elephant men")
        self.assertEqual("elephant-men", regex)

    def test_pattern_0(self):
        regex = transform_text_pattern("why are elephants")
        self.assertEqual("why-are-", regex)

    def test_pattern_1(self):
        regex = transform_text_pattern("why can elephants")
        self.assertEqual("why-can-", regex)

    def test_pattern_2(self):
        regex = transform_text_pattern("why is elephant")
        self.assertEqual("why-is-", regex)

    def test_pattern_3(self):
        regex = transform_text_pattern("why can't elephants")
        self.assertEqual("why-can_t-", regex)

    def test_pattern_4(self):
        regex = transform_text_pattern("why do elephants")
        self.assertEqual("why-do-", regex)

    def test_pattern_5(self):
        regex = transform_text_pattern("why does elephant")
        self.assertEqual("why-does-", regex)

    def test_pattern_6(self):
        regex = transform_text_pattern("how does elephant")
        self.assertEqual("how-does-", regex)

    def test_pattern_7(self):
        regex = transform_text_pattern("why elephant")
        self.assertIn("why", regex)
        self.assertNotIn("elephant", regex)
        self.assertIn("[^", regex)


if __name__ == '__main__':
    unittest.main()
