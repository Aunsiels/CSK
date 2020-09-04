import unittest

from quasimodo.data_structures.inputs import Inputs
from quasimodo.assertion_generation.openie_fact_generator_submodule import OpenIEFactGeneratorSubmodule
from quasimodo.patterns.pattern_google import PatternGoogle
from quasimodo.data_structures.referencable_interface import ReferencableInterface
from quasimodo.statement_maker import StatementMaker


class TestOpenIEFactGenerator(unittest.TestCase):

    def setUp(self) -> None:
        dummy_reference = ReferencableInterface("Dummy reference")
        self.openie_fact_generator = OpenIEFactGeneratorSubmodule(dummy_reference)
        self.openie_fact_generator.statement_maker = StatementMaker(use_cache=False)
        self.openie_fact_generator._name = "OPENIE"  # Dummy name only useful for testing
        self.empty_input = Inputs()

    def test_no_suggestion(self):
        new_gfs = self.openie_fact_generator.get_generated_facts([])
        self.assertEqual(len(new_gfs), 0)

    def test_one_suggestion(self):
        suggestion = ("why do lions eat zebras", 1.0, None, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "lions")
        self.assertEqual(new_gfs[0].get_predicate(), "eat")
        self.assertEqual(new_gfs[0].get_object(), "zebras")

    def test_one_suggestion_with_a(self):
        suggestion = ("why does a lion eat zebras", 1.0, None, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "lion")
        self.assertEqual(new_gfs[0].get_predicate(), "eat")
        self.assertEqual(new_gfs[0].get_object(), "zebras")

    def test_one_suggestion_with_the(self):
        suggestion = ("why does the lion eat zebras", 1.0, None, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "lion")
        self.assertEqual(new_gfs[0].get_predicate(), "eat")
        self.assertEqual(new_gfs[0].get_object(), "zebras")

    def test_very_short_suggestion(self):
        suggestion = ("why do lions eat", 1.0, None, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "lions")
        self.assertEqual(new_gfs[0].get_predicate(), "can")
        self.assertEqual(new_gfs[0].get_object(), "eat")

    def test_can_short_suggestion(self):
        suggestion = ("why can lions eat", 1.0, None, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "lions")
        self.assertEqual(new_gfs[0].get_predicate(), "can")
        self.assertEqual(new_gfs[0].get_object(), "eat")

    def test_cannot_short_suggestion(self):
        suggestion = ("why cannot lions eat", 1.0, None, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "lions")
        self.assertEqual(new_gfs[0].get_predicate(), "can")
        self.assertEqual(new_gfs[0].get_object(), "eat")
        self.assertTrue(new_gfs[0].is_negative())

    def test_cannot_short_suggestion_pattern(self):
        pattern = PatternGoogle("why cannot", "can", True)
        suggestion = ("why cannot lions eat", 1.0, pattern, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "lions")
        self.assertEqual(new_gfs[0].get_predicate(), "can")
        self.assertEqual(new_gfs[0].get_object(), "eat")
        self.assertTrue(new_gfs[0].is_negative())

    def test_arent_short_suggestion_pattern(self):
        pattern = PatternGoogle("why aren't", "ARN'T", True)
        suggestion = ("why aren't lions fat", 1.0, pattern, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "lions")
        self.assertEqual(new_gfs[0].get_predicate(), "are")
        self.assertEqual(new_gfs[0].get_object(), "fat")
        self.assertTrue(new_gfs[0].is_negative())

    def test_cannot_short_suggestion1(self):
        suggestion = ("why can't lions eat", 1.0, None, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "lions")
        self.assertEqual(new_gfs[0].get_predicate(), "can")
        self.assertEqual(new_gfs[0].get_object(), "eat")
        self.assertTrue(new_gfs[0].is_negative())

    def test_can_short_suggestion_1(self):
        suggestion = ("why can a lion eat", 1.0, None, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "a lion")
        self.assertEqual(new_gfs[0].get_predicate(), "can")
        self.assertEqual(new_gfs[0].get_object(), "eat")

    def test_short_incorrect_suggestion(self):
        suggestion = ("why do lion proutkoko eat", 1.0, None, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 0)

    def test_single_can_suggestion(self):
        suggestion = ("why can lion", 1.0, None, "lion")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 0)

    def test_extend(self):
        suggestion = ("why do african people have noses and lips", 1.0, None, "african people")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 3)
        objs = list(map(lambda x: x.get_object(), new_gfs))
        self.assertIn("noses", objs)
        self.assertIn("lips", objs)

    def test_extend_2(self):
        suggestion = ("why are pandas black and white", 1.0, None, "pandas")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 2)
        objs = list(map(lambda x: x.get_object(), new_gfs))
        self.assertIn("black", objs)
        self.assertIn("white", objs)

    def test_than(self):
        suggestion = ("why are elephants better than lions", 1.0, None, "elephants")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "elephants")
        self.assertEqual(new_gfs[0].get_predicate(), "are better than")
        self.assertEqual(new_gfs[0].get_object(), "lions")

    def test_long_object(self):
        suggestion = ("why do elephants have long noses", 1.0, None, "elephants")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertTrue(len(new_gfs) >= 2)
        objs = list(map(lambda x: x.get_object(), new_gfs))
        self.assertIn("noses", objs)
        self.assertIn("long noses", objs)

    def test_long_object_with_multiple_modalities(self):
        suggestion = ("why do african elephants have long noses", 1.0, None, "elephants")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertTrue(len(new_gfs) >= 2)
        objs = list(map(lambda x: x.get_object(), new_gfs))
        self.assertIn("noses", objs)
        self.assertIn("long noses", objs)
        self.assertIn("TBC[", new_gfs[0].get_modality().get())
        self.assertIn("some[", new_gfs[0].get_modality().get())
        self.assertIn("long noses", new_gfs[0].get_modality().get())

    def test_are_not(self):
        suggestion = ("why are elephants not in africa", 1.0, None, "elephants")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertTrue(len(new_gfs) >= 1)
        self.assertEqual(new_gfs[0].get_subject(), "elephants")
        self.assertEqual(new_gfs[0].get_predicate(), "are in")
        self.assertEqual(new_gfs[0].get_object(), "africa")
        self.assertTrue(new_gfs[0].is_negative())

    def test_is_not(self):
        suggestion = ("why is thomas not in africa", 1.0, None, "thomas")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertTrue(len(new_gfs) >= 1)
        self.assertEqual(new_gfs[0].get_subject(), "thomas")
        self.assertEqual(new_gfs[0].get_predicate(), "is in")
        self.assertEqual(new_gfs[0].get_object(), "africa")
        self.assertTrue(new_gfs[0].is_negative())

    def test_there(self):
        suggestion = ("why are there elephants in africa", 1.0, None, "elephants")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertTrue(len(new_gfs) >= 1)
        self.assertEqual(new_gfs[0].get_subject(), "elephants")
        self.assertEqual(new_gfs[0].get_predicate(), "are in")
        self.assertEqual(new_gfs[0].get_object(), "africa")
        self.assertFalse(new_gfs[0].is_negative())

    def test_does(self):
        suggestion = ("why does panda climb tree", 1.0, None, "panda")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertTrue(len(new_gfs) >= 1)
        self.assertEqual(new_gfs[0].get_subject(), "panda")
        self.assertEqual(new_gfs[0].get_predicate(), "climb")
        self.assertEqual(new_gfs[0].get_object(), "tree")

    def test_always(self):
        suggestion = ("why does pandas climb always in tree", 1.0, None, "panda")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertTrue(len(new_gfs) >= 1)
        self.assertEqual(new_gfs[0].get_subject(), "pandas")
        self.assertEqual(new_gfs[0].get_predicate(), "always climb in")
        self.assertEqual(new_gfs[0].get_object(), "tree")

    def test_can_simple_ignore(self):
        suggestion = ("why does leather quality", 1.0, None, "leather")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertTrue(len(new_gfs) == 0)

    def test_can_simple_not_ignore(self):
        suggestion = ("why does leather die", 1.0, None, "leather")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs),  1)
        self.assertEqual(new_gfs[0].get_subject(), "leather")
        self.assertEqual(new_gfs[0].get_predicate(), "can")
        self.assertEqual(new_gfs[0].get_object(), "die")

    def test_ing_simple(self):
        suggestion = ("why is drinking coffee bad", 1.0, None, "drinking coffee")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs),  1)
        self.assertEqual(new_gfs[0].get_subject(), "drinking coffee")
        self.assertEqual(new_gfs[0].get_predicate(), "is")
        self.assertEqual(new_gfs[0].get_object(), "bad")

    def test_ing_after_verb(self):
        suggestion = ("why do vegetarians go back to eating meat",
                      1.0, None, "vegetarian")
        new_gfs = self.openie_fact_generator._openie_from_file([suggestion])
        self.assertEqual(len(new_gfs),  1)
        self.assertEqual(new_gfs[0].get_subject(), "vegetarians")
        self.assertNotEqual(new_gfs[0].get_object(), "meat")

    def test_complex_subject(self):
        suggestion = ("why are japanese things cute", 1.0, None, "thing")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        self.assertEqual(len(new_gfs),  1)
        self.assertEqual(new_gfs[0].get_subject(), "japanese things")
        self.assertEqual(new_gfs[0].get_object(), "cute")

    def test_fart(self):
        suggestion = ("why do farts smell worse in the shower",
                      1.0, None, "farts")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        print(new_gfs)
        self.assertEqual(len(new_gfs),  1)
        self.assertEqual(new_gfs[0].get_subject(), "farts")

    def test_baby(self):
        suggestion = ("how are babies actually made",
                      1.0, None, "baby")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        print(new_gfs)
        self.assertEqual(len(new_gfs),  2)
        self.assertEqual(new_gfs[0].get_subject(), "babies")

    def _test_poop(self):
        suggestion = ("why do dogs poop in kennel",
                      1.0, None, "dog")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        print(new_gfs)
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(new_gfs[0].get_subject(), "dog")
        self.assertEqual(new_gfs[0].get_predicate(), "poop in")

    def test_baby_from_file(self):
        suggestion = ("how are babies actually made",
                      1.0, None, "baby")
        new_gfs = self.openie_fact_generator._openie_from_file([suggestion])
        print(new_gfs)
        # Here the object is empty
        self.assertEqual(len(new_gfs),  0)
        self.assertEqual(new_gfs[0].get_subject(), "babies")


if __name__ == '__main__':
    unittest.main()
