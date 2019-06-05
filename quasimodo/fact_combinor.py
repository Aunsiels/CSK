from quasimodo.multiple_pattern import MultiplePattern
from .submodule_interface import SubmoduleInterface


def read_sentence(sentence):
    res = []
    sentence_parts = sentence.split(" // ")
    for part in sentence_parts:
        part_score = part.split("x#x")
        if len(part_score) == 1:
            res.append((part_score[0].strip(), 1))
        else:
            res.append((part_score[0].strip(), int(part_score[1])))
    return res


class FactCombinor(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Fact Combinor"

    def process(self, input_interface):
        found = dict()
        sentences = dict()
        modalities = dict()
        patterns = dict()
        for generated_fact in input_interface.get_generated_facts():
            fact = generated_fact.get_fact()
            modality = fact.get_modality()
            if modality is not None:
                modality = modality.get()
            else:
                modality = ""
            fact = fact.change_modality("")
            pattern = generated_fact.get_pattern()
            sentence_source = generated_fact.get_sentence_source()
            if fact in found:
                found[fact].get_score().add(generated_fact.get_score())
            else:
                found[fact] = generated_fact
                sentences[fact] = dict()
                modalities[fact] = dict()
                patterns[fact] = MultiplePattern()
            if len(sentence_source) > 0:
                for sentence, score in read_sentence(sentence_source):
                    sentences[fact][sentence] = sentences[fact].get(sentence, 0) + score
            if len(modality) > 0:
                for modality_temp, score in read_sentence(modality):
                    modalities[fact][modality_temp] = modalities[fact].get(modality_temp, 0) + score
            patterns[fact].add_pattern(pattern)
        new_gfs = []
        for fact in found:
            generated_fact = found[fact]
            new_sentence = " // ".join([x[0] + " x#x" + str(x[1]) for x in sentences[fact].items()])
            new_modality = " // ".join([x[0] + " x#x" + str(x[1]) for x in modalities[fact].items()])
            new_gfs.append(generated_fact.change_sentence(new_sentence)
                           .change_modality(new_modality)
                           .change_pattern(patterns[fact]))
        return input_interface.replace_generated_facts(new_gfs)
