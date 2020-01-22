import json

from quasimodo.data_structures.inputs import Inputs
from quasimodo.data_structures.module_reference_interface import ModuleReferenceInterface
from quasimodo.data_structures.subject import Subject
from quasimodo.default_submodule_factory import DefaultSubmoduleFactory


def run_for_subject(subject):

    factory = DefaultSubmoduleFactory()

    submodule_generation_names = [
        "google-autocomplete",
        "bing-autocomplete",
        "yahoo-questions",
        "answerscom-questions",
        "quora-questions",
        "reddit-questions",
        "fact-combinor",
    ]

    submodule_normalization_names = [
        "lower-case",
        "tbc-cleaner",
        "only-subject",
        "no-personal",
        "singular-subject",
        "cleaning-predicate",
        "basic-modality",
        "present-continuous",
        "are-transformation",
        "can-transformation",
        "filter-object",
        "be-normalization",
        "identical-subj-obj",
        "present-conjugate"
    ]

    submodule_normalization_global_names = [
        "similar-object-remover",
        "fact-combinor"
    ]

    submodule_validation_names = [
        "google-book",
        "flickr-clusters",
        "imagetag",
        "wikipedia-cooccurrence",
        "simple-wikipedia-cooccurrence",
        "conceptual-captions",
        "what-questions"
    ]

    empty_input = Inputs()
    empty_input = empty_input.add_subjects({Subject(subject.lower())})

    module_reference = ModuleReferenceInterface("")

    result = []

    result.append(dict())
    result[-1]["step name"] = "Assertion Generation"
    result[-1]["steps"] = []
    generated_facts = []
    for submodule_name in submodule_generation_names:
        submodule = factory.get_submodule(submodule_name, module_reference)
        input_temp = submodule.process(empty_input)
        generated_facts += input_temp.get_generated_facts()
        step_info = dict()
        step_info["name"] = submodule.get_name()
        step_info["facts"] = [x.to_dict() for x in input_temp.get_generated_facts()]
        result[-1]["steps"].append(step_info)
    new_input = empty_input.add_generated_facts(generated_facts)

    result.append(dict())
    result[-1]["step name"] = "Assertion Normalization"
    result[-1]["steps"] = []
    for submodule_name in submodule_normalization_names:
        submodule = factory.get_submodule(submodule_name, module_reference)
        step_info = dict()
        step_info["name"] = submodule.get_name()
        step_info["modifications"] = []
        for generated_fact in new_input.get_generated_facts():
            input_temp = empty_input.add_generated_facts([generated_fact])
            input_temp = submodule.process(input_temp)
            if len(input_temp.get_generated_facts()) != 1 or input_temp.get_generated_facts()[0] != generated_fact:
                modification = {
                    "from": generated_fact.to_dict(),
                    "to": [x.to_dict() for x in input_temp.get_generated_facts()]
                }
                step_info["modifications"].append(modification)
        result[-1]["steps"].append(step_info)
        new_input = submodule.process(new_input)

    result.append(dict())
    result[-1]["step name"] = "Assertion Normalization Global"
    result[-1]["steps"] = []
    for submodule_name in submodule_normalization_global_names:
        submodule = factory.get_submodule(submodule_name, module_reference)
        new_input = submodule.process(new_input)
        step_info = dict()
        step_info["name"] = submodule.get_name()
        step_info["facts"] = [x.to_dict() for x in new_input.get_generated_facts()]
        result[-1]["steps"].append(step_info)

    result.append(dict())
    result[-1]["step name"] = "Assertion Validation"
    result[-1]["steps"] = []
    for submodule_name in submodule_validation_names:
        submodule = factory.get_submodule(submodule_name, module_reference)
        new_input = submodule.process(new_input)
    step_info = dict()
    step_info["name"] = "All validations"
    step_info["facts"] = [x.to_dict() for x in new_input.get_generated_facts()]
    result[-1]["steps"].append(step_info)

    print(json.dumps(result))