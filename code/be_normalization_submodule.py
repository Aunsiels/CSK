from submodule_interface import SubmoduleInterface
import logging


class BeNormalizationSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Be Normalization"

    def process(self, input_interface):
        logging.info("normalize the form of be")
        new_gfs = []
        for gf in input_interface.get_generated_facts():
            pred = gf.get_predicate().get()
            if pred.startswith("is ") or pred.startswith("are ") or\
                    pred == "is" or pred == "are":
                pred = pred.split(" ")
                pred[0] = "be"
                pred = " ".join(pred)
                new_gfs.append(gf.change_predicate(pred))
            else:
                new_gfs.append(gf)
        return input_interface.replace_generated_facts(new_gfs)
