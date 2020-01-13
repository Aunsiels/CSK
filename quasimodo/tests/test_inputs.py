import json
import unittest

from quasimodo.fact import Fact
from quasimodo.generated_fact import GeneratedFact
from quasimodo.inputs import Inputs
from quasimodo.module_reference_interface import ModuleReferenceInterface
from quasimodo.multiple_module_reference import MultipleModuleReference
from quasimodo.multiple_pattern import MultiplePattern
from quasimodo.multiple_scores import MultipleScore
from quasimodo.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.multiple_submodule_reference import MultipleSubmoduleReference
from quasimodo.object import Object
from quasimodo.pattern_google import PatternGoogle
from quasimodo.subject import Subject
from quasimodo.submodule_reference_interface import SubmoduleReferenceInterface


class TestInput(unittest.TestCase):

    def test_serialize_multiple_source_occurrence(self):
        msr = MultipleSubmoduleReference(SubmoduleReferenceInterface("Submodule0"))
        msr.add_reference(SubmoduleReferenceInterface("Submodule0"))
        mso = MultipleSourceOccurrence.from_raw("baba is you", msr, 1)
        print(mso.to_dict())
        self.assertIsNotNone(json.dumps(mso.to_dict()))

    def test_save(self):
        inputs = Inputs()
        subjects = [Subject("baba"), Subject("coko")]
        patterns = [PatternGoogle("why are"),
                    PatternGoogle("Why are", "hasProperty", True)]
        mmr = MultipleModuleReference(ModuleReferenceInterface("Module0"))
        mmr.add_reference(ModuleReferenceInterface("Module1"))
        msr = MultipleSubmoduleReference(SubmoduleReferenceInterface("Submodule0"))
        msr.add_reference(SubmoduleReferenceInterface("Submodule0"))
        ms0 = MultipleScore()
        ms0.add_score(1.0, ModuleReferenceInterface("Module0"), SubmoduleReferenceInterface("Submodule0"))
        ms1 = MultipleScore()
        ms1.add_score(1.0, mmr, msr)
        ms1.add_score(0.5, ModuleReferenceInterface("Module1"), SubmoduleReferenceInterface("Submodule2"))
        mp0 = MultiplePattern()
        mp0.add_pattern(patterns[0])
        mp1 = MultiplePattern()
        mp1.add_pattern(patterns[0])
        mp1.add_pattern(patterns[1])
        gfs = [
            GeneratedFact(
                "baba",
                "is",
                "you",
                "sometimes",
                False,
                ms0,
                MultipleSourceOccurrence.from_raw("baba is you", msr, 1),
                mp0
            ),
            GeneratedFact(
                "coko",
                "is",
                "dead",
                "always",
                True,
                ms1,
                MultipleSourceOccurrence.from_raw("toto is always dead", msr, 1),
                mp1
            )
        ]
        seeds = [
            Fact(
                "baba",
                "is",
                "us",
                None,
                False
            ),
            Fact(
                "coko",
                "are",
                "missing",
                "coucou",
                True
            )
        ]
        objects = [Object("missing"), Object("you")]
        inputs = inputs.replace_seeds(seeds)
        inputs = inputs.replace_patterns(patterns)
        inputs = inputs.replace_subjects(subjects)
        inputs = inputs.replace_generated_facts(gfs)
        inputs = inputs.replace_objects(objects)
        inputs.save("temp.json")
        inputs_read = inputs.load("temp.json")
        self.assertEqual(len(inputs.get_generated_facts()), len(inputs_read.get_generated_facts()))
        self.assertEqual(len(inputs.get_subjects()), len(inputs_read.get_generated_facts()))
        self.assertEqual(len(inputs.get_patterns()), len(inputs_read.get_patterns()))
        self.assertEqual(len(inputs.get_seeds()), len(inputs_read.get_seeds()))
        self.assertEqual(len(inputs.get_objects()), len(inputs_read.get_objects()))


if __name__ == '__main__':
    unittest.main()
