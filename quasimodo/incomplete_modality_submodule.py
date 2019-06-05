from .submodule_interface import SubmoduleInterface
import logging


class IncompleteModalitySubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Incomplete Modality"

    def process(self, input_interface):
        logging.info("Start the incomplete modality processing")
        gfs = input_interface.get_generated_facts()
        # group by subject
        gf_subj = dict()
        for gf in gfs:
            subj = gf.get_subject().get()
            if subj in gf_subj:
                gf_subj[subj].append(gf)
            else:
                gf_subj[subj] = [gf]
        new_gfs = []
        for subj in gf_subj:
            # for each object, we check if it appears in a predicate
            for gf0 in gf_subj[subj]:
                found = False
                obj0 = gf0.get_object().get()
                for gf1 in gf_subj[subj]:
                    obj1 = gf1.get_object().get()
                    if (obj0 in gf1.get_predicate().get()
                        or (obj0 in obj1 and obj0 != obj1)) and\
                            gf0.get_predicate().get() in \
                            gf1.get_predicate().get():
                        # Modify modality
                        found = True
                        modality = "TBC"
                        if gf0.has_modality():
                            modality += " " + gf0.get_modality().get()
                        new_gfs.append(gf0.change_modality(modality))
                        break
                if not found:
                    new_gfs.append(gf0)
        return input_interface.replace_generated_facts(new_gfs)
