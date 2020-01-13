import json

from quasimodo.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.pattern_google import PatternGoogle
from quasimodo.multiple_module_reference import MultipleModuleReference
from quasimodo.multiple_pattern import MultiplePattern
from quasimodo.multiple_submodule_reference import MultipleSubmoduleReference
from quasimodo.object import Object
from quasimodo.predicate import Predicate
from quasimodo.subject import Subject
from quasimodo.modality import Modality
from quasimodo.module_reference_interface import ModuleReferenceInterface
from quasimodo.submodule_reference_interface import SubmoduleReferenceInterface
from quasimodo.multiple_scores import MultipleScore
from quasimodo.fact import Fact
from quasimodo.generated_fact import GeneratedFact


class UnknownSerializedObject(NameError):
    def __init__(self, message):
        self.message = message


def read_seeds(seeds):
    return [read_seed(x) for x in seeds]


def read_pattern(pattern):
    if pattern["type"] == "NO_PATTERN":
        return None
    if pattern["type"] == "MultiplePattern":
        multiple_pattern = MultiplePattern()
        for pattern_temp in pattern["patterns"]:
            multiple_pattern.add_pattern(read_pattern(pattern_temp))
        return multiple_pattern
    if pattern["type"] == "PatternGoogle":
        return PatternGoogle(pattern["prefix"], pattern["relation"], pattern["negative"])
    raise UnknownSerializedObject("Unknown pattern type" + json.dumps(pattern))


def read_patterns(patterns):
    return [read_pattern(x) for x in patterns]


def read_predicate(predicate):
    if predicate["type"] == "Predicate":
        return Predicate(predicate["value"])
    raise UnknownSerializedObject("Unknown predicate type:" + json.dumps(predicate))


def read_object(obj):
    if obj["type"] == "Object":
        return Object(obj["value"])
    raise UnknownSerializedObject("Unknown object type:" + json.dumps(obj))


def read_modality(modality):
    if modality["type"] == "NO_MODALITY":
        return None
    if modality["type"] == "Modality":
        return Modality(modality["value"])
    raise UnknownSerializedObject("Unknown modality type:" + json.dumps(modality))


def read_module_reference(module_reference):
    if module_reference["type"] == "MultipleModuleReference":
        multiple_module_reference = MultipleModuleReference()
        for reference in module_reference["references"]:
            multiple_module_reference.add_reference(read_module_reference(reference))
        return multiple_module_reference
    if module_reference["type"] == "ModuleReference":
        return ModuleReferenceInterface(module_reference["name"])
    raise UnknownSerializedObject("Unknown module reference type:" + json.dumps(module_reference))


def read_submodule_reference(submodule_reference):
    if submodule_reference["type"] == "MultipleSubmoduleReference":
        multiple_submodule_reference = MultipleSubmoduleReference()
        for reference in submodule_reference["references"]:
            multiple_submodule_reference.add_reference(read_submodule_reference(reference))
        return multiple_submodule_reference
    if submodule_reference["type"] == "SubmoduleReference":
        return SubmoduleReferenceInterface(submodule_reference["name"])
    raise UnknownSerializedObject("Unknown module reference type:" + json.dumps(submodule_reference))


def read_score(score):
    if score["type"] == "MultipleScore":
        multiple_score = MultipleScore()
        for score_temp in score["scores"]:
            multiple_score.add_score(
                score_temp["score"],
                read_module_reference(score_temp["module_from"]),
                read_submodule_reference(score_temp["submodule_from"])
            )
        return multiple_score
    raise UnknownSerializedObject("Unknown score type:" + json.dumps(score))


def read_generated_fact(generated_fact):
    if generated_fact["type"] == "GeneratedFact":
        return GeneratedFact(
            read_subject(generated_fact["subject"]),
            read_predicate(generated_fact["predicate"]),
            read_object(generated_fact["object"]),
            read_modality(generated_fact["modality"]),
            generated_fact["negative"],
            read_score(generated_fact["score"]),
            MultipleSourceOccurrence.from_dict(generated_fact["sentence_source"]),
            read_pattern(generated_fact["pattern"])
        )
    raise UnknownSerializedObject("Unknown generated fact type" + json.dumps(generated_fact))


def read_generated_facts(generated_facts):
    return [read_generated_fact(x) for x in generated_facts]


def read_subjects(subjects):
    return [read_subject(x) for x in subjects]


def read_objects(objects):
    return [read_object(x) for x in objects]


def read_subject(subject):
    if subject["type"] == "Subject":
        return Subject(subject["value"])
    raise UnknownSerializedObject("Unknown subject type:" + json.dumps(subject))


def read_seed(seed):
    if seed["type"] == "Fact":
        return Fact(
            read_subject(seed["subject"]),
            read_predicate(seed["predicate"]),
            read_object(seed["object"]),
            read_modality(seed["modality"]),
            seed["negative"])
    raise UnknownSerializedObject("Unknown seed type" + json.dumps(seed))

