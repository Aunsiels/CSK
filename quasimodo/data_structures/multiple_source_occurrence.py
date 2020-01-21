import json


class MultipleSourceOccurrence(object):

    def __init__(self):
        self.occurrences = dict()

    @classmethod
    def from_raw(cls, text, source, n_occurrences):
        mso = MultipleSourceOccurrence()
        mso.add_raw(text, source, n_occurrences)
        return mso

    def add_raw(self, text, source, n_occurrences=1):
        if text not in self.occurrences:
            self.occurrences[text] = dict()
            self.occurrences[text]["sources"] = []
            self.occurrences[text]["n_occurrences"] = 0
        if source not in self.occurrences[text]["sources"]:
            self.occurrences[text]["sources"].append(source)
        self.occurrences[text]["n_occurrences"] += n_occurrences

    def get_total_number_occurrences(self):
        total = 0
        for text in self.occurrences:
            total += self.occurrences[text]["n_occurrences"]
        return total

    def to_dict(self):
        res = dict()
        res["type"] = "MultipleSourceOccurrence"
        res["occurrences"] = dict()
        for key in self.occurrences:
            res["occurrences"][key] = dict()
            res["occurrences"][key]["sources"] = [source.to_dict() for source in self.occurrences[key]["sources"]]
            res["occurrences"][key]["n_occurrences"] = self.occurrences[key]["n_occurrences"]
        return res

    def __add__(self, other):
        mso = MultipleSourceOccurrence()
        for mso_temp in [self, other]:
            for key in mso_temp.occurrences:
                occurrences = mso_temp.occurrences[key]["n_occurrences"]
                for source in mso_temp.occurrences[key]["sources"]:
                    mso.add_raw(key, source, occurrences)
                    occurrences = 0
        return mso

    @classmethod
    def from_dict(cls, dictionary):
        from quasimodo.serialized_object_reader import UnknownSerializedObject, read_submodule_reference
        mso = MultipleSourceOccurrence()
        if dictionary["type"] == "MultipleSourceOccurrence":
            for key in dictionary["occurrences"]:
                mso.occurrences[key] = dict()
                mso.occurrences[key]["sources"] = [read_submodule_reference(source)
                                                   for source in dictionary["occurrences"][key]["sources"]]
                mso.occurrences[key]["occurrences"] = dictionary["occurrences"][key]["n_occurrences"]
            return mso
        raise UnknownSerializedObject("Unknown module reference type:" + json.dumps(dictionary))

    def __str__(self):
        sentences = []
        for key in self.occurrences:
            sentences.append(key + " x#x" + str(self.occurrences[key]["n_occurrences"]) + " x#x" +
                             ", ".join([source.get_name() for source in self.occurrences[key]["sources"]
                                        if source is not None]))
        return " // ".join(sentences)
