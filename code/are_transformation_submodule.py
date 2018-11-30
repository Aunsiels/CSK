from submodule_interface import SubmoduleInterface
from nltk.corpus import wordnet as wn
import logging

exceptions = ["black"]

class AreTransformationSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Are transformation"

    def _replace_are(self, gfs):
        new_gfs = []
        for gf in gfs:
            if gf.get_predicate().get() != "are" and\
                    gf.get_predicate().get() != "is":
                new_gfs.append(gf)
            elif gf.get_pattern() is not None and\
                    gf.get_pattern().get_relation() is not None:
                new_gfs.append(gf.change_predicate(
                    gf.get_pattern().get_relation()))
            else:
                new_gfs.append(gf)
        return new_gfs

    def _get_attr(self, gfs):
        new_gfs = []
        attr = wn.synsets("attribute")[1]
        for gf in gfs:
            if gf.get_predicate().get() != "are" and\
                    gf.get_predicate().get() != "is":
                new_gfs.append(gf)
            else:
                # TODO Preprocessing on the object
                obj_synsets = wn.synsets(gf.get_object().get())
                paths = []
                for entity in obj_synsets:
                    for path in entity.hypernym_paths():
                        if attr in path:
                            paths.append(path)

                new_preds = []
                for path in paths:
                    found_attr = False
                    new_predicate = None
                    for synset in path:
                        if not found_attr and synset != attr:
                            continue
                        elif synset == attr:
                            found_attr = True
                        elif not found_attr:
                            continue
                        elif "property" in synset.name():
                            continue
                        else:
                            new_predicate = synset
                            break
                    if new_predicate is not None and\
                            new_predicate not in new_preds:
                        new_preds.append(new_predicate)

                if len(new_preds) != 1 and \
                        gf.get_object().get() not in exceptions:
                    new_gfs.append(gf)
                else:
                    new_predicate = new_preds[0]
                    name = new_predicate.name()
                    name = name[:name.find(".")]
                    new_gfs.append(gf.change_predicate("has_" + name))
        return new_gfs

    def _get_part(self, gfs):
        new_gfs = []
        # part = wn.synsets("part")[2]
        part = wn.synsets("body_part")[0]
        for gf in gfs:
            if gf.get_predicate().get() != "are" and\
                    gf.get_predicate().get() != "have" and\
                    gf.get_predicate().get() != "is":
                new_gfs.append(gf)
            else:
                obj_synsets = wn.synsets(gf.get_object().get())
                paths = []
                for entity in obj_synsets:
                    for path in entity.hypernym_paths():
                        if part in path:
                            paths.append(path)
                if paths:
                    new_gfs.append(gf.change_predicate("has_physical_part"))
                else:
                    new_gfs.append(gf)
        return new_gfs

    def process(self, input_interface):
        logging.info("Start the are predicate transformation")
        gfs = input_interface.get_generated_facts()
        gfs = self._get_attr(gfs)
        gfs = self._get_part(gfs)
        gfs = self._replace_are(gfs)
        return input_interface.replace_generated_facts(gfs)
