from .module_reference_interface import ModuleReferenceInterface


class MultipleModuleReference(ModuleReferenceInterface):

    def __init__(self, module_reference=None):
        super().__init__("")
        if module_reference is None:
            self._name = ""
            self._references = []
        else:
            self._name = module_reference.get_name()
            self._references = [module_reference]

    def add_reference(self, module_reference):
        self._references.append(module_reference)
        self._name = "; ".join(set([x.get_name() for x in self._references if x is not None]))

    def is_from(self, module_name):
        return any([x.get_name() == module_name for x in self._references if x is not None])

    def to_dict(self):
        res = dict()
        res["type"] = "MultipleModuleReference"
        res["references"] = []
        for reference in self._references:
            res["references"].append(reference.to_dict())
        return res
