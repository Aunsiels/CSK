from quasimodo.data_structures.submodule_interface import SubmoduleInterface
import logging


class ToLowerCaseSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "To lower Case"

    def process(self, input_interface):
        logging.info("Start the lowering case")

        new_gfs = []
        for gf in input_interface.get_generated_facts():
            subj = gf.get_subject().get().lower()
            pred = gf.get_predicate().get().lower()
            obj = gf.get_object().get().lower()
            new_gf = gf.change_subject(subj)\
                       .change_object(obj)\
                       .change_predicate(pred)
            new_gfs.append(new_gf)
        return input_interface.replace_generated_facts(new_gfs)
