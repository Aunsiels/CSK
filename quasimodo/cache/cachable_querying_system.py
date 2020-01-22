from quasimodo.parameters_reader import ParametersReader

parameters_reader = ParametersReader()
PATTERN_FIRST = (parameters_reader.get_parameter("pattern-first") or "true") == "true"
possible_second_word_question = ["is", "are", "do", "does", "can", "can_t", "isn_t", "aren_t", "doesn_t", "don_t"]


def get_regex_from_query(filename):
    # Remove the pattern to be get more results
    if PATTERN_FIRST:
        filename_regex = get_regex_from_query_by_pattern(filename)
    else:
        filename_regex = get_regex_from_query_by_subject(filename)
    return filename_regex


def get_regex_from_query_by_subject(filename):
    filename_split = filename.split("-")
    if len(filename_split) <= 1:
        filename_regex = filename
    else:
        if filename_split[0] in ["why", "how"]:
            if filename_split[1] in possible_second_word_question and len(filename_split) >= 3:
                if filename_split[2][-1] == "s":
                    filename_split[2] = filename_split[2][:-1]
                filename_regex = "-".join(filename_split[2:])
            else:
                filename_regex = "-".join(filename_split[1:])
        else:
            filename_regex = filename
    return filename_regex


def get_regex_from_query_by_pattern(filename):
    filename_split = filename.split("-")
    if len(filename_split) <= 1:
        filename_regex = filename
    else:
        if filename_split[0] in ["why", "how"]:
            if filename_split[1] in possible_second_word_question:
                filename_regex = "-".join(filename_split[:2]) + "-"
            else:
                filename_regex = filename_split[0] + "-[^" + "|".join(possible_second_word_question) + "][^-]*-"
        else:
            filename_regex = filename
    return filename_regex


def to_filename(query):
    filename = query.replace(" ", "-").replace("'", "_").replace("/", "-")
    return filename


class CachableQueryingSystem:

    def __init__(self, cache):
        self.local_cache = {}
        self.cache = cache

    def read_cache(self, query):
        filename = to_filename(query)
        if filename in self.local_cache:
            return self.local_cache[filename], True
        else:
            filename_regex = get_regex_from_query(filename)
            if self.local_cache.get("query_regex", "") != filename_regex:
                self.local_cache = self.cache.read_regex(filename_regex)
                self.local_cache["query_regex"] = filename_regex
        if filename in self.local_cache:
            return self.local_cache[filename], True
        return None

    def write_cache(self, query, suggestions):
        filename = to_filename(query)
        self.cache.write_cache(filename, suggestions)
