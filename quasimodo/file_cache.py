import os
import shutil


class FileCache(object):

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir + "/"
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def write_cache(self, query, suggestions):
        filename = self.cache_dir + query.replace(" ", "-").replace("'", "_").replace("/", "-")
        with open(filename, "w") as f:
            for suggestion in suggestions:
                f.write(str(suggestion[0]) + "\t" + str(suggestion[1]) + "\n")

    def read_cache(self, query):
        filename = self.cache_dir + query.replace(" ", "-").replace("'", "_").replace("/", "-")
        if os.path.isfile(filename):
            suggestions = []
            with open(filename) as f:
                for line in f:
                    suggestion = line.strip().split("\t")
                    suggestions.append((suggestion[0], float(suggestion[1])))
            return suggestions, True
        else:
            return None

    def delete_cache(self):
        # Only delete if we are sure it is a test
        if "test" in self.cache_dir:
            shutil.rmtree(self.cache_dir, ignore_errors=True)

    def read_regex(self, regex):
        raise NotImplementedError