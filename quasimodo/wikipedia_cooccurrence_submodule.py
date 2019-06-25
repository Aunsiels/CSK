from quasimodo.content_comparator import ContentComparator
from quasimodo.mongodb_cache import MongoDBCache
from quasimodo.parameters_reader import ParametersReader
import logging
import wikipedia

parameters_reader = ParametersReader()
DEFAULT_MONGODB_LOCATION = parameters_reader.get_parameter("default-mongodb-location") or "mongodb://localhost:27017/"


class WikipediaCooccurrenceSubmodule(ContentComparator):

    def __init__(self, module_reference, use_cache=True, cache_name="wikipedia-cache"):
        super().__init__(module_reference)
        self._name = "Wikipedia Cooccurrence"
        self.use_cache = use_cache
        self._lang = "en"
        self.cache = MongoDBCache(cache_name, mongodb_location=DEFAULT_MONGODB_LOCATION)

    def _get_wikipedia_page_content(self, name):
        content = self.read_cache(name)
        if content is not None:
            return content
        search = wikipedia.search(name)
        # For now, we only consider the first result
        if search:
            try:
                content = wikipedia.page(search[0]).content
            except wikipedia.DisambiguationError as e:
                # Not clear how often it happens
                if e.options:
                    try:
                        content = wikipedia.page(e.options[0]).content
                    except wikipedia.DisambiguationError as e2:
                        if e2.options:
                            temp = e2.options[0].replace("(", "")\
                                .replace(")", "")
                            try:
                                content = wikipedia.page(temp).content
                            except wikipedia.DisambiguationError as e3:
                                pass
                            except wikipedia.exceptions.PageError:
                                logging.warning("Wikipedia page not found: " + name)
                    except wikipedia.exceptions.PageError:
                        logging.warning("Wikipedia page not found: " + name)
            except wikipedia.exceptions.PageError:
                logging.warning("Wikipedia page not found: " + name)
        self.write_cache(name, content)
        return content

    def write_cache(self, wikipedia_page, content):
        if self.use_cache:
            filename = wikipedia_page.replace(" ", "_").replace("/", "_")
            self.cache.write_cache(filename, content)

    def read_cache(self, wikipedia_page):
        if self.use_cache:
            filename = wikipedia_page.replace(" ", "_").replace("/", "_")
            cache_value = self.cache.read_cache(filename)
            if cache_value is not None:
                return cache_value[0]
        return None

    def get_contents(self, subject):
        return [self._get_wikipedia_page_content(subject)]

    def setup_processing(self):
        wikipedia.set_lang(self._lang)


