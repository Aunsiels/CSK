import json
import logging
import unittest

from quasimodo import serialized_object_reader
from quasimodo.data_structures.subject import Subject

logging.basicConfig(level=logging.DEBUG)

from quasimodo.data_structures.inputs import Inputs
from quasimodo.default_module_factory import DefaultModuleFactory
from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.multiple_scores import MultipleScore
from quasimodo.data_structures.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.patterns.pattern_google import PatternGoogle


class TestComplete(unittest.TestCase):

    def test_first(self):
        empty_input = Inputs()
        logging.info("Starting complete test for normalization")
        gf = GeneratedFact("elephant", "are", "blue?", "", False, MultipleScore(),
                           MultipleSourceOccurrence(), PatternGoogle(""))
        subjects = {gf.get_subject()}
        input = empty_input.add_subjects(subjects).add_generated_facts([gf])
        factory = DefaultModuleFactory()
        normalization_module = factory.get_module("assertion-normalization")
        new_input = normalization_module.process(input)
        new_gfs = new_input.get_generated_facts()
        self.assertEqual(1, len(new_gfs))
        self.assertEqual("elephant", new_gfs[0].get_subject().get())
        self.assertEqual("has_property", new_gfs[0].get_predicate().get())
        self.assertEqual("blue", new_gfs[0].get_object().get())

    def test_normalize_beach(self):
        empty_input = Inputs()
        logging.info("Starting complete test for normalization")
        gf = GeneratedFact("beaches", "have", "sand", "", False,
                           MultipleScore(),
                           MultipleSourceOccurrence(), PatternGoogle(""))
        subjects = {Subject("beach")}
        input = empty_input.add_subjects(subjects).add_generated_facts([gf])
        factory = DefaultModuleFactory()
        normalization_module = factory.get_module("assertion-normalization")
        new_input = normalization_module.process(input)
        new_gfs = new_input.get_generated_facts()
        self.assertEqual(1, len(new_gfs))

    def test_normalize_babies(self):
        empty_input = Inputs()
        logging.info("Starting complete test for normalization")
        gf = GeneratedFact("babies", "are ", "made", "TBC[actually made]",
                           False,
                           MultipleScore(),
                           MultipleSourceOccurrence(), PatternGoogle(""))
        subjects = {Subject("baby")}
        input = empty_input.add_subjects(subjects).add_generated_facts([gf])
        factory = DefaultModuleFactory()
        normalization_module = factory.get_module("assertion-normalization")
        new_input = normalization_module.process(input)
        new_gfs = new_input.get_generated_facts()
        self.assertEqual(1, len(new_gfs))
        self.assertEqual(new_gfs[0].get_predicate(), "has_property")

    def test_normalize_can(self):
        empty_input = Inputs()
        logging.info("Starting complete test for normalization")
        gf = GeneratedFact("nafcil", "can", "nafcillin", "",
                           False,
                           MultipleScore(),
                           MultipleSourceOccurrence(), PatternGoogle(""))
        subjects = {Subject("nafcil")}
        input = empty_input.add_subjects(subjects).add_generated_facts([gf])
        factory = DefaultModuleFactory()
        normalization_module = factory.get_module("assertion-normalization")
        new_input = normalization_module.process(input)
        new_gfs = new_input.get_generated_facts()
        self.assertEqual(0, len(new_gfs))

    def test_normalize_all_beach_sand(self):
        gfs = []
        with open("beach.jsonl") as f:
            for line in f:
                json_line = json.loads(line.strip())
                gfs.append(serialized_object_reader.read_generated_fact(
                    json_line)
                )
        self.assertTrue(len(gfs) > 1)
        empty_input = Inputs()
        subjects = {Subject("beach")}
        input = empty_input.add_subjects(subjects).add_generated_facts(gfs)
        factory = DefaultModuleFactory()
        normalization_module = factory.get_module("assertion-normalization")
        new_input = normalization_module.process(input)
        new_gfs = new_input.get_generated_facts()
        self.assertTrue(len(new_gfs) > 1)
        gfs_have = [x for x in new_gfs
                    if x.get_subject().get() == "beach"
                    and x.get_predicate().get() == "have"
                    and x.get_object().get() == "sand"]
        self.assertTrue(len(gfs_have), 1)
