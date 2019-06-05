from .submodule_reference_interface import SubmoduleReferenceInterface


class MultipleSubmoduleReference(SubmoduleReferenceInterface):

    def __init__(self, submodule_reference):
        self._name = submodule_reference.get_name()
        self._references = [submodule_reference]

    def add_reference(self, submodule_reference):
        self._references.append(submodule_reference)
        self._name = "; ".join(set([x.get_name() for x in self._references]))

    def is_from(self, submodule_name):
        return any([x.get_name() == submodule_name for x in self._references])
