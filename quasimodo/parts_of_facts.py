from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.modality import read_sentence, Modality
from quasimodo.data_structures.multiple_module_reference import MultipleModuleReference
from quasimodo.data_structures.multiple_pattern import MultiplePattern
from quasimodo.data_structures.multiple_scores import MultipleScore
from quasimodo.data_structures.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.data_structures.multiple_submodule_reference import MultipleSubmoduleReference


class PartsOfFacts(object):

    def __init__(self):
        self.found = dict()
        self.sentences = dict()
        self.modalities = dict()
        self.patterns = dict()
        self.modules = dict()
        self.submodules = dict()
        self.all_submodules = set()

    def initialize_for_generated_fact(self, generated_fact):
        fact_without_modality = get_fact_without_modality(generated_fact)
        if fact_without_modality not in self.found:
            self.found[fact_without_modality] = None
            self.sentences[fact_without_modality] = MultipleSourceOccurrence()
            self.modalities[fact_without_modality] = dict()
            self.patterns[fact_without_modality] = MultiplePattern()
            self.modules[fact_without_modality] = MultipleModuleReference()
            self.submodules[fact_without_modality] = MultipleSubmoduleReference()

    def add_score(self, generated_fact):
        fact_without_modality = get_fact_without_modality(generated_fact)
        if self.found[fact_without_modality] is None:
            self.found[fact_without_modality] = generated_fact
        else:
            self.found[fact_without_modality].get_score().add(generated_fact.get_score())

    def add_sentence_source(self, generated_fact):
        fact_without_modality = get_fact_without_modality(generated_fact)
        self.sentences[fact_without_modality] += generated_fact.get_sentence_source()

    def add_modality(self, generated_fact):
        fact = generated_fact.get_fact()
        fact_without_modality = get_fact_without_modality(generated_fact)
        if len(get_modality(fact)) > 0:
            for modality_temp, score in read_sentence(get_modality(fact)):
                self.modalities[fact_without_modality][modality_temp] = \
                    self.modalities[fact_without_modality].get(modality_temp, 0) + score

    def add_pattern(self, generated_fact):
        fact_without_modality = get_fact_without_modality(generated_fact)
        self.patterns[fact_without_modality].add_pattern(generated_fact.get_pattern())

    def add_modules(self, generated_fact):
        fact_without_modality = get_fact_without_modality(generated_fact)
        for _, module_source, _ in generated_fact.get_score().scores:
            self.modules[fact_without_modality].add_reference(module_source)

    def add_submodules(self, generated_fact):
        fact_without_modality = get_fact_without_modality(generated_fact)
        for score, _, submodules_source in generated_fact.get_score().scores:
            self.submodules[fact_without_modality].add_reference(submodules_source)
            self.all_submodules.add(submodules_source)

    def update(self, generated_fact):
        self.initialize_for_generated_fact(generated_fact)
        self.add_score(generated_fact)
        self.add_sentence_source(generated_fact)
        self.add_modality(generated_fact)
        self.add_pattern(generated_fact)
        self.add_modules(generated_fact)
        self.add_submodules(generated_fact)

    @staticmethod
    def from_generated_facts(generated_facts):
        parts_of_facts = PartsOfFacts()
        for generated_fact in sorted(generated_facts,
                                     key=predicate_to_number):
            parts_of_facts.update(generated_fact)
        return parts_of_facts

    def merge_into_generated_facts(self):
        new_gfs = []
        for fact_without_modality in self.found:
            generated_fact = self.found[fact_without_modality]
            new_modality = Modality.from_modalities_and_scores(self.modalities[fact_without_modality].items())
            new_gfs.append(generated_fact.change_sentence(self.sentences[fact_without_modality])
                           .change_modality(new_modality)
                           .change_pattern(self.patterns[fact_without_modality]))
        return new_gfs

    def get_all_submodules(self):
        return self.all_submodules

    def get_tbc_score(self, fact):
        number_tbc = 0
        total = 0
        for modality_raw in self.modalities[fact]:
            total += self.modalities[fact][modality_raw]
            if "TBC" in modality_raw:
                number_tbc += self.modalities[fact][modality_raw]
        if total > 0:
            if total == number_tbc:
                return 1.0
        return 0.0

    def get_fact_row(self, fact):
        result = [fact.get_subject().get(), fact.get_predicate().get(), fact.get_object().get()]
        modality = Modality.from_modalities_and_scores(self.modalities[fact].items())
        if modality:
            result.append(modality)
        else:
            result.append(" ")
        if fact.is_negative():
            result.append(1)
        else:
            result.append(0)
        result.append(self.patterns[fact].to_str())
        names = self.get_all_submodules()
        scores_per_submodules = dict()
        for score, _, name in self.found[fact].get_score().scores:
            if name in names:
                scores_per_submodules[name] = score
        for name in names:
            if name in scores_per_submodules:
                result.append(scores_per_submodules[name])
            else:
                result.append("")
        result.append(self.sentences[fact].get_total_number_occurrences())
        result.append(sum(self.modalities.get(fact, dict()).values()))
        return result

    def get_header(self):
        temp = ["subject", "predicate", "object", "modality", "is negative", "patterns"]
        for submodule in self.get_all_submodules():
            temp.append(submodule.get_name())
        temp.append("number sentences")
        temp.append("number modalities")
        return temp

    def get_generated_fact_with_score_from_classifier(self, fact, clf):
        multiple_score = MultipleScore()
        row = self.get_fact_row(fact)
        score = clf.predict(fact, row)
        multiple_score.add_score(score, self.modules[fact], self.submodules[fact])
        return GeneratedFact(
            fact.get_subject(),
            fact.get_predicate(),
            fact.get_object(),
            Modality.from_modalities_and_scores(self.modalities[fact].items()),
            fact.is_negative(),
            multiple_score,
            self.sentences[fact],
            self.patterns[fact])

    def get_all_facts(self):
        return self.found.keys()


def get_fact_without_modality(generated_fact):
    return generated_fact.get_fact().change_modality("")


def get_modality(fact):
    modality = fact.get_modality()
    if modality is not None:
        modality = modality.get()
    else:
        modality = ""
    return modality


PREPOSITIONS = {"aboard", "about", "above", "across", "after", "against",
                "along", "amid", "among", "anti", "around", "as", "at",
                "before", "behind", "below", "beneath", "beside", "besides",
                "between", "beyond", "but", "by", "concerning", "considering",
                "despite", "down", "during", "except", "excepting",
                "excluding", "following", "for", "from", "in", "inside",
                "into", "like", "minus", "near", "of", "off", "on", "onto",
                "opposite", "outside", "over", "past", "per", "plus",
                "regarding", "round", "save", "since", "than", "through", "to",
                "toward", "towards", "under", "underneath", "unlike", "until",
                "up", "upon", "versus", "via", "with", "within", "without"}


def predicate_to_number(generated_fact):
    # Lowest score have the priority during merging
    # For example, if "be in" is before "be", then "be, in school" becomes
    # "be in, school"
    predicate = str(generated_fact.get_predicate())
    if predicate == "has_property":
        return 0
    if predicate.startswith("has_"):
        return -10000
    predicate_s = predicate.split(" ")
    # We do not want predicate that are too long
    # With 4, we can have predicate with a comparison like
    # be more interesting than
    if len(predicate_s) > 4 or predicate_s[-1] not in PREPOSITIONS:
        return len(predicate)
    return -len(predicate)
