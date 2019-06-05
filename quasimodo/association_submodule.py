from .submodule_interface import SubmoduleInterface
import logging


def _get_maximum_score(associations):
    maxi = 0
    for word0 in associations:
        for word1 in associations[word0]:
            maxi = max(maxi, associations[word0][word1])
    return maxi


class AssociationSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Association submodule"

    def _get_associations(self, subjects):
        """__get_assos
        :return: dictionary of dictionary, d[s0][s1] is the number of
        associations between s0 and s1"""
        raise NotImplementedError

    def process(self, input_interface):
        logging.info("Start the association submodule for " + self.get_name())
        associations = self._get_associations(input_interface.get_subjects())
        maxi = _get_maximum_score(associations)
        for generated_facts in input_interface.get_generated_facts():
            subject = generated_facts.get_subject().get()
            obj = generated_facts.get_object().get()
            if subject in associations and obj in associations[subject]:
                new_score = associations[subject][obj] / maxi
                generated_facts.get_score().add_score(new_score, self._module_reference, self)
        return input_interface
