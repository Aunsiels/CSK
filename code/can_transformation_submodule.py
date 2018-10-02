from submodule_interface import SubmoduleInterface
import logging


class CanTransformationSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Can Transformation"

    def process(self, input_interface):
        logging.info("Start the transformation of can predicates")
        new_gfs = []
        for gf in input_interface.get_generated_facts():
            # Correct OPENIE output
            if gf.get_predicate().get() == "can" and\
                    gf.get_object().get()[:4] == "can "\
                    and gf.get_object().get()[:7] != "can be ":
                new_gfs.append(gf.change_object(gf.get_object().get()
                                                .replace("can ", "be ")))
            elif gf.get_predicate().get() == "be":
                temp = gf
                if gf.get_object().get()[:4] == "can ":
                   temp = temp.change_object(gf.get_object().get()
                                               .replace("can ", ""))
                if gf.get_pattern() is not None and\
                        "why can" in gf.get_pattern().to_str():
                   temp = temp.change_predicate("can be")
                new_gfs.append(temp)
            else:
                new_gfs.append(gf)
        return input_interface.replace_generated_facts(new_gfs)
