from submodule_interface import SubmoduleInterface
from inputs import Inputs
from pattern_google import PatternGoogle

class ManualPatternsGoogleSubmodule(SubmoduleInterface):
    """ManualPatternsGoogleSubmodule
    A submodule which output patterns manually entered
    """

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Manual patterns google"

    def process(self, input_interface):
        new_patterns = []
        new_patterns.append(PatternGoogle("why are <SUBJS>"))
        new_patterns.append(PatternGoogle("why do <SUBJS>"))
        return input_interface.add_patterns(new_patterns)
