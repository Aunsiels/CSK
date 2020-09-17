import logging

from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.data_structures.subject import Subject


# From https://www.engvid.com/english-resource/the-with-country-names-lakes-rivers/
COUNTRIES = ["the Bahamas", "the Cayman Islands",
             "the Central African Republic", "the Channel Islands",
             "the Comoros", "the Czech Republic", "the Dominican Republic",
             "the Falkland Islands", "the Gambia",
             "the Isle of Man", "the Ivory Coast",
             "the Leeward Islands", "the Maldives",
             "the Marshall Islands", "the Netherlands",
             "the Netherlands Antilles", "the Philippines",
             "the Solomon Islands", "the Turks and Caicos Islands",
             "the United Arab Emirates", "the United Kingdom",
             "the uk", "the United States of America",
             "the us", "the usa",
             "the Virgin Islands",
             ]

RIVERS = ["the Amazon",
          "the Colorado", "the Columbia", "the Danube", "the Don",
          "the Euphrates", "the Ganges", "the Huang", "the Hudson",
          "the Indus", "the Jordan", "the Lena", "the Mackenzie", "the Mekong",
          "the Mississippi", "the Missouri", "the Niger", "the Nile", "the Ob",
          "the Ohio", "the Orinoco", "the Po", "the Rhine", "the Rhone",
          "the Rio Grande", "the St. Lawrence", "the Seine", "the Tagus",
          "the Thames", "the Tiber", "the Tigris", "the Volga", "the Yangtze"]

SEAS = ["the Adriatic Sea", "the Aegean Sea", "the Arabian Sea",
        "the Arctic Ocean",
        "the Atlantic", "the Baltic", "the Black Sea",
        "the Caribbean", "the Caspian", "the Coral Sea",
        "the Gulf of Aden", "the Gulf of Mexico", "the Gulf of Oman "]

MONTS = ["the Alps", "the Andes", "the Appalachians", "the Atlas Mountains",
         "the Caucasus", "the Himalayas", "the Pyrenees", "the Rockies",
         "the Urals"]

OTHERS = ["the equator", "the Far East", "the Gobi", "the Kalahari",
          "the Middle East", "the Near East", "the North Pole", "the Occident",
          "the Orient", "the Panama Canal", "the Sahara", "the South Pole",
          "the Suez Canal", "the Tropic of Cancer", "the Tropic of Capricorn"]


class SpecialSubjects(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Special subjects"

    def process(self, input_interface):
        logging.info("Start special subjects")
        subjects = COUNTRIES + SEAS + RIVERS + MONTS + OTHERS
        subjects = [Subject(x.lower()) for x in subjects]
        return input_interface.add_subjects(subjects)
