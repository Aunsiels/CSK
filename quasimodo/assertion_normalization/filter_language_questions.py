from quasimodo.data_structures.submodule_interface import SubmoduleInterface
import logging

LANGUAGES = {"chinese", "mandarin", "spanish", "english", "hindi",
             "bengali", "portuguese", "russian", "japanese",
             "western punjabi", "marathi", "telugu", "wu", "turkish",
             "korean", "french", "german", "vietnamese", "tamil", "yue",
             "urdu", "javanese", "italian", "egyptian Arabic", "gujarati",
             "iranian Persian", "bhojpuri", "min nan", "hakka", "jin", "hausa",
             "kannada", "indonesian", "polish", "yoruba", "xiang", "malayalam",
             "odia", "maithili", "burmese", "eastern punjabi", "sunda",
             "sudanese arabic", "algerian arabic", "moroccan arabic", "arabic",
             "ukrainian", "igbo", "northern Uzbek", "sindhi",
             "north levantine arabic", "romanian", "tagalog", "dutch",
             "saʽidi arabic", "gan", "amharic", "northern pashto", "magahi",
             "thai", "saraiki", "khmer", "chhattisgarhi", "somali", "malay",
             "cebuano", "nepali", "mesopotamian arabic", "assamese",
             "sinhalese", "northern kurdish", "hejazi arabic",
             "nigerian fulfulde", "bavarian", "south azerbaijani", "greek",
             "chittagonian", "kazakh", "deccan", "hungarian", "kinyarwanda",
             "zulu", "south levantine arabic", "tunisian arabic",
             "sanaani spoken arabic", "min bei", "southern pashto", "rundi",
             "czech", "taʽizzi-adeni arabic", "uyghur", "min dong", "sylheti"
             }


class FilterLanguageQuestions(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Filter language questions"

    def process(self, input_interface):
        logging.info("Start filtering the language questions")
        new_generated_facts = []
        for g in input_interface.get_generated_facts():
            predicate = g.get_predicate().get()
            obj = g.get_object().get()
            if predicate != "be in" or obj not in LANGUAGES:
                new_generated_facts.append(g)
        return input_interface.replace_generated_facts(new_generated_facts)
