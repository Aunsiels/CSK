from module_reference_interface import ModuleReferenceInterface

class MultipleModuleReference(ModuleReferenceInterface):

    def __init__(self, module_reference):
        self._name = module_reference.get_name()
        self._references = [module_reference]

    def add_reference(self, module_reference):
        self._references.append(module_reference)
        self._name = "; ".join(set([x.get_name() for x in self._references]))

    def is_from(self, module_name):
        return any([x.get_name() == module_name for x in self._references])
