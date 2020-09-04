from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.patterns.pattern_google import PatternGoogle
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
        new_patterns = [PatternGoogle("why aren't <SUBJS>", relation="has_property", negative=True),
                        PatternGoogle("why are <SUBJS>", relation="has_property"),
                        PatternGoogle("why is <SUBJ>", relation="has_property"),
                        PatternGoogle("why is a <SUBJ>",
                                      relation="has_property"),
                        PatternGoogle("why isn't <SUBJ>", relation="has_property", negative=True),
                        PatternGoogle("why isn't a <SUBJ>",
                                      relation="has_property", negative=True),
                        PatternGoogle("why do <SUBJS>"),
                        PatternGoogle("why does a <SUBJS>"),
                        PatternGoogle("why does <SUBJ>"),
                        PatternGoogle("why don't <SUBJS>", negative=True),
                        PatternGoogle("why doesn't <SUBJ>", negative=True),
                        PatternGoogle("why doesn't a <SUBJ>", negative=True),
                        PatternGoogle("why can <SUBJS>", "CAN"),
                        PatternGoogle("why can a <SUBJ>", "CAN"),
                        PatternGoogle("why can't <SUBJS>", "CAN", True),
                        PatternGoogle("why can't a <SUBJ>", "CAN", True),
                        PatternGoogle("how are <SUBJS>", relation="has_property"),
                        PatternGoogle("how is <SUBJ>", relation="has_property"),
                        PatternGoogle("how is a <SUBJ>",
                                      relation="has_property"),
                        PatternGoogle("how do <SUBJS>"),
                        PatternGoogle("how does <SUBJ>"),
                        PatternGoogle("how does a <SUBJ>"),
                        PatternGoogle("how can <SUBJS>", "CAN"),
                        PatternGoogle("how can a <SUBJS>", "CAN"),
                        PatternGoogle("why <SUBJ>"),
                        PatternGoogle("why a <SUBJ>")]
        return input_interface.add_patterns(new_patterns)
