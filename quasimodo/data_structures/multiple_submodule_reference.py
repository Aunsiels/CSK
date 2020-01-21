from .submodule_reference_interface import SubmoduleReferenceInterface


class MultipleSubmoduleReference(SubmoduleReferenceInterface):

    def __init__(self, submodule_reference=None):
        super().__init__("")
        if submodule_reference is None:
            self._name = ""
            self._references = []
        else:
            self._name = submodule_reference.get_name()
            self._references = [submodule_reference]

    def add_reference(self, submodule_reference):
        self._references.append(submodule_reference)
        self._name = "; ".join(set([x.get_name() for x in self._references if x is not None]))

    def is_from(self, submodule_name):
        return any([x.get_name() == submodule_name for x in self._references if x is not None])

    def to_dict(self):
        res = dict()
        res["type"] = "MultipleSubmoduleReference"
        res["references"] = []
        for reference in self._references:
            res["references"].append(reference.to_dict())
        return res
