import unittest

from quasimodo import Inputs, PatternGoogle
from quasimodo.default_module_factory import DefaultModuleFactory
from quasimodo.generated_fact import GeneratedFact
from quasimodo.multiple_scores import MultipleScore


class TestComplete(unittest.TestCase):

    def test_first(self):
        empty_input = Inputs()
        gf = GeneratedFact("elephant", "are", "blue?", "", False, MultipleScore(), "", PatternGoogle(""))
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