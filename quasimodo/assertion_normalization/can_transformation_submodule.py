from quasimodo.data_structures.submodule_interface import SubmoduleInterface
import logging


def transform_generated_fact(generated_fact):
    new_generated_fact = generated_fact
    predicate = generated_fact.get_predicate().get()
    obj = generated_fact.get_object().get()
    if predicate == "can" and obj[:4] == "can ":
        if obj[:7] != "can be ":
            new_generated_fact = generated_fact.change_object(obj.replace("can ", ""))
        else:
            new_generated_fact = generated_fact.change_object(obj.replace("can be ", "")) \
                .change_predicate("can be")
    elif predicate == "be":
        if obj[:4] == "can ":
            new_generated_fact = new_generated_fact.change_object(obj.replace("can ", ""))
        if generated_fact.get_pattern() is not None and \
                "why can" in generated_fact.get_pattern().to_str():
            new_generated_fact = new_generated_fact.change_predicate("can be")
    return new_generated_fact


class CanTransformationSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Can Transformation"

    def process(self, input_interface):
        logging.info("Start the transformation of can predicates")
        new_gfs = []
        for generated_fact in input_interface.get_generated_facts():
            # Correct OPENIE output
            new_generated_fact = transform_generated_fact(generated_fact)
            new_gfs.append(new_generated_fact)
        return input_interface.replace_generated_facts(new_gfs)
