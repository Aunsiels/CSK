from quasimodo.generated_fact import GeneratedFact
from quasimodo.modality import read_sentence, get_multiple_parts_combination, Modality
from quasimodo.multiple_module_reference import MultipleModuleReference
from quasimodo.multiple_pattern import MultiplePattern
from quasimodo.multiple_scores import MultipleScore
from quasimodo.multiple_submodule_reference import MultipleSubmoduleReference


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
            self.sentences[fact_without_modality] = dict()
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
        if len(generated_fact.get_sentence_source()) > 0:
            for sentence, score in read_sentence(generated_fact.get_sentence_source()):
                self.sentences[fact_without_modality][sentence] = \
                    self.sentences[fact_without_modality].get(sentence, 0) + score

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
        for generated_fact in generated_facts:
            parts_of_facts.update(generated_fact)
        return parts_of_facts

    def merge_into_generated_facts(self):
        new_gfs = []
        for fact_without_modality in self.found:
            generated_fact = self.found[fact_without_modality]
            new_sentence = get_multiple_parts_combination(self.sentences[fact_without_modality].items())
            new_modality = Modality.from_modalities_and_scores(self.modalities[fact_without_modality].items())
            new_gfs.append(generated_fact.change_sentence(new_sentence)
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
        result.append(sum(self.sentences[fact].values()))
        return result

    def get_header(self):
        temp = ["subject", "predicate", "object", "modality", "is negative", "patterns"]
        for submodule in self.get_all_submodules():
            temp.append(submodule.get_name())
        temp.append("number sentences")
        return temp

    def get_combined_sentence(self, fact):
        return get_multiple_parts_combination(self.sentences[fact].items())

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
            self.get_combined_sentence(fact),
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
