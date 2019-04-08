from submodule_interface import SubmoduleInterface
import logging


class AssociationSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Association submodule"

    def _get_assos(self, subjects):
        """__get_assos
        :return: dictionary of dictionary, d[s0][s1] is the number of
        associations between s0 and s1"""
        raise NotImplementedError

    def _get_max(self, d):
        maxi = 0
        for s0 in d:
            for s1 in d[s0]:
                maxi = max(maxi, d[s0][s1])
        return maxi

    def process(self, input_interface):
        logging.info("Start the association submodule for " + self.get_name())
        new_generated_facts = []
        assos = self._get_assos(input_interface.get_subjects())
        maxi = self._get_max(assos)
        new_generated_facts = []
        for g in input_interface.get_generated_facts():
            if g.get_module_source().get_name() == self._module_reference.get_name():
                continue
            subj = g.get_subject().get()
            obj = g.get_object().get()
            if subj in assos and obj in assos[subj]:
                new_score = assos[subj][obj] / maxi
                new_generated_facts.append(g.change_score(new_score)
                                           .change_module_source(
                                               self._module_reference)
                                           .change_submodule_source(
                                               self).remove_sentence())
        return input_interface.add_generated_facts(new_generated_facts)
