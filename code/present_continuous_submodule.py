from submodule_interface import SubmoduleInterface
import logging
from nltk.stem import WordNetLemmatizer


class PresentContinuousSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "No Present Continuous"

    def process(self, input_interface):
        logging.info("Start the cleaning of present continuous")
        new_generated_facts = []
        lemmatizer = WordNetLemmatizer()
        for g in input_interface.get_generated_facts():
            predicate = g.get_predicate().get()
            pred_l = predicate.split(" ")
            if len(pred_l) > 1 and pred_l[0] == "are" and \
                    "ing" == pred_l[1][-3:]:
                new_generated_facts.append(
                    g.change_predicate((lemmatizer.lemmatize(pred_l[1], pos="v")
                                       + " " + " ".join(pred_l[2:])).strip()))
            else:
                new_generated_facts.append(g)
        return input_interface.replace_generated_facts(new_generated_facts)
