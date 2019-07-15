import pymongo


def transform_query(query):
    return query.replace(" ", "-").replace("'", "_").replace("/", "-")


class MongoDBCache(object):

    def __init__(self, collection_name, mongodb_location="mongodb://localhost:27017/"):
        self.collection_name = collection_name
        mongodb_client = pymongo.MongoClient(mongodb_location)
        self.database = mongodb_client["CSKDB"]
        self.collection = None
        self.create_collection()

    def create_collection(self):
        self.collection = self.database[self.collection_name]

    def exists_collection(self):
        return self.collection_name in self.database.list_collection_names()

    def delete_cache(self):
        if "test" in self.collection_name and self.collection is not None:
            self.collection.drop()
            self.collection = None

    def write_cache(self, query, suggestions):
        query = transform_query(query)
        self.collection.update_one({"query": query}, {"$set": {"suggestions": suggestions}}, upsert=True)

    def write_many_cache(self, query_suggestions):
        database_entry = map(lambda x: {"query": transform_query(x[0]), "suggestions": x[1]}, query_suggestions)
        self.collection.insert_many(database_entry)

    def read_cache(self, query):
        query = transform_query(query)
        database_query = {"query": query}
        result = self.collection.find_one(database_query, {"suggestions": 1})
        if result:
            return result["suggestions"]
        return None

    def read_regex(self, query_regex):
        database_query = {"query": {"$regex": query_regex}}
        results = self.collection.find(database_query)
        return self.results_to_query_dictionary(results)

    def read_all(self):
        results = self.collection.find()
        return self.results_to_query_dictionary(results)

    def results_to_query_dictionary(self, results):
        d_results = {}
        for result in results:
            d_results[result["query"]] = result["suggestions"]
        return d_results
