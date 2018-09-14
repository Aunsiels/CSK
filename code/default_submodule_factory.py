from submodule_factory_interface import SubmoduleFactoryInterface
from submodule_google_autocomplete import SubmoduleGoogleAutocomplete
from animal_submodule import AnimalSubmodule
from manual_patterns_google_submodule import ManualPatternsGoogleSubmodule
from bing_autocomplete_submodule import BingAutocompleteSubmodule

class DefaultSubmoduleFactory(SubmoduleFactoryInterface):
    """DefaultSubmoduleFactory
    The default submodule factory
    """

    def get_submodule(self, submodule_name, module_reference):
        if submodule_name == "google-autocomplete":
            return SubmoduleGoogleAutocomplete(module_reference)
        elif submodule_name == "animal-seeds":
            return AnimalSubmodule(module_reference)
        elif submodule_name == "manual-patterns-google":
            return ManualPatternsGoogleSubmodule(module_reference)
        elif submodule_name == "bing-autocomplete":
            return BingAutocompleteSubmodule(module_reference)
        else:
            raise NotImplementedError
