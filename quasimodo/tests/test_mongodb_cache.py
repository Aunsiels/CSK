import unittest

from quasimodo.cache.mongodb_cache import MongoDBCache


class TestMongoDBCache(unittest.TestCase):

    def test_creation(self):
        cache = MongoDBCache("test")
        self.assertFalse(cache.exists_collection())
        cache.write_cache("test", [])
        self.assertTrue(cache.exists_collection())
        cache2 = MongoDBCache("test")
        self.assertTrue(cache2.exists_collection())
        cache.delete_cache()
        self.assertFalse(cache.exists_collection())
        self.assertFalse(cache2.exists_collection())

    def test_write_read(self):
        cache = MongoDBCache("testrw")
        cache.delete_cache()
        cache = MongoDBCache("testrw")
        cache_value = cache.read_cache("elephant")
        self.assertIsNone(cache_value)
        cache.write_cache("elephant", [["elephants are big", 0]])
        cache_value = cache.read_cache("elephant")
        self.assertIsNotNone(cache_value)
        suggestions = cache_value
        self.assertEqual([["elephants are big", 0]], suggestions)
        cache.delete_cache()

    def _test_write_read_other(self):
        cache = MongoDBCache("testrw", mongodb_location="YOURLOCATION")
        cache_value = cache.read_cache("elephant")
        self.assertIsNone(cache_value)
        cache.write_cache("elephant", [("elephants are big", 0)])
        cache_value = cache.read_cache("elephant")
        self.assertIsNotNone(cache_value)
        suggestions = cache_value
        self.assertEqual(["elephants are big"], suggestions)
        cache.delete_cache()


if __name__ == '__main__':
    unittest.main()
