import time

from rq import get_current_job

from quasimodo.data_structures.inputs import Inputs
from quasimodo.data_structures.module_reference_interface import ModuleReferenceInterface
from quasimodo.data_structures.subject import Subject
from quasimodo.default_submodule_factory import DefaultSubmoduleFactory


def run_for_subject(subject):
    job = get_current_job()

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
        "filter-object",
        "no-personal",
        "singular-subject",
        "cleaning-predicate",
        "basic-modality",
        "present-continuous",
        "are-transformation",
        "can-transformation",
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

    pattern_submodule = factory.get_submodule("manual-patterns-google", module_reference)
    empty_input = pattern_submodule.process(empty_input)

    result = []

    result.append(dict())
    result[-1]["step name"] = "Assertion Generation"
    result[-1]["steps"] = []
    job.meta = result
    job.save_meta()
    generated_facts = []
    for submodule_name in submodule_generation_names:
        submodule = factory.get_submodule(submodule_name, module_reference)
        begin_time = time.time()
        input_temp = submodule.process(empty_input)
        generated_facts += input_temp.get_generated_facts()
        step_info = dict()
        step_info["name"] = submodule.get_name()
        step_info["facts"] = [x.to_dict() for x in input_temp.get_generated_facts()]
        step_info["time"] = time.time() - begin_time
        result[-1]["steps"].append(step_info)
        job.meta = result
        job.save_meta()
    new_input = empty_input.add_generated_facts(generated_facts)

    result.append(dict())
    result[-1]["step name"] = "Assertion Normalization"
    result[-1]["steps"] = []
    for submodule_name in submodule_normalization_names:
        submodule = factory.get_submodule(submodule_name, module_reference)
        step_info = dict()
        begin_time = time.time()
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
        step_info["time"] = time.time() - begin_time
        result[-1]["steps"].append(step_info)
        job.meta = result
        job.save_meta()
        new_input = submodule.process(new_input)

    result.append(dict())
    result[-1]["step name"] = "Assertion Normalization Global"
    result[-1]["steps"] = []
    for submodule_name in submodule_normalization_global_names:
        submodule = factory.get_submodule(submodule_name, module_reference)
        begin_time = time.time()
        new_input = submodule.process(new_input)
        step_info = dict()
        step_info["name"] = submodule.get_name()
        step_info["facts"] = [x.to_dict() for x in new_input.get_generated_facts()]
        step_info["time"] = time.time() - begin_time
        result[-1]["steps"].append(step_info)
        job.meta = result
        job.save_meta()

    result.append(dict())
    result[-1]["step name"] = "Assertion Validation"
    result[-1]["steps"] = []
    begin_time = time.time()
    for submodule_name in submodule_validation_names:
        submodule = factory.get_submodule(submodule_name, module_reference)
        new_input = submodule.process(new_input)
    step_info = dict()
    step_info["name"] = "All validations"
    step_info["facts"] = [x.to_dict() for x in new_input.get_generated_facts()]
    step_info["time"] = time.time() - begin_time
    result[-1]["steps"].append(step_info)
    job.meta = result
    job.save_meta()
