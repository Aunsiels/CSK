from .submodule_interface import SubmoduleInterface
from .pattern_google import PatternGoogle
import logging


class ManualPatternsGoogleSubmodule(SubmoduleInterface):
    """ManualPatternsGoogleSubmodule
    A submodule which output patterns manually entered
    """

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Manual patterns google"

    def process(self, input_interface):
        logging.info("Start the manual patterns for browsers submodule")
        new_patterns = [PatternGoogle("why are <SUBJS>"), PatternGoogle("why is <SUBJ>"),
                        PatternGoogle("why do <SUBJS>"), PatternGoogle("why does <SUBJ>"),
                        PatternGoogle("why can <SUBJS>", "CAN"), PatternGoogle("how are <SUBJS>"),
                        PatternGoogle("how is <SUBJ>"), PatternGoogle("how do <SUBJS>"),
                        PatternGoogle("how does <SUBJ>"), PatternGoogle("how can <SUBJS>", "CAN"),
                        PatternGoogle("why can't <SUBJS>", "CAN", True),
                        PatternGoogle("why <SUBJ>")]
        return input_interface.add_patterns(new_patterns)
