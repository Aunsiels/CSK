import unittest

from quasimodo.inputs import Inputs
from quasimodo.bing_autocomplete_submodule import BingAutocompleteSubmodule
from quasimodo.conceptual_captions_comparator_submodule import ConceptualCaptionsComparatorSubmodule
from quasimodo.generated_fact import GeneratedFact
from quasimodo.google_autocomplete_submodule import GoogleAutocompleteSubmodule
from quasimodo.multiple_scores import MultipleScore
from quasimodo.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.referencable_interface import ReferencableInterface
from quasimodo.subject import Subject


class TestSentenceComparator(unittest.TestCase):

    def test_get_content(self):
        sc = ConceptualCaptionsComparatorSubmodule(None)
        self.empty_input = Inputs()
        subjects = {Subject("elephant"), Subject("penguin"), Subject("lion"), Subject("raccoon")}
        inputs = self.empty_input.add_subjects(subjects)
        sc.setup_processing(inputs)
        contents = sc.get_contents("elephant")
        self.assertEqual(3748, len(contents))
        contents = sc.get_contents("penguin")
        self.assertEqual(1273, len(contents))
        contents = sc.get_contents("lion")
        self.assertEqual(2616, len(contents))
        contents = sc.get_contents("raccoon")
        self.assertEqual(365, len(contents))

    def test_conceptual_caption(self):
        sc = ConceptualCaptionsComparatorSubmodule(None)
        self.empty_input = Inputs()
        self.dummy_reference = ReferencableInterface("DUMMY")

        dataset = [("elephant", "download", "baby", 0),
                   ("elephant", "have", "tusks", 1),
                   ("lion", "eat", "gazella", 0),
                   ("penguin", "eat", "fish", 0),
                   ("gorilla", "eat", "banana", 0),
                   ("sky", "hasProperty", "blue", 0),
                   ("computer", "is", "working", 1),
                   ("raccoon", "hasProperty", "blue", 0)
                   ]
        subjects = {Subject("elephant"), Subject("penguin"), Subject("lion"),
                    Subject("gorilla"), Subject("sky"), Subject("computer"),
                    Subject("raccoon")}

        gfs = []
        pos = 0
        for subject, predicate, obj, truth in dataset:
            pos += 1
            score = MultipleScore()
            if pos % 2 == 0:
                score.add_score(truth, self.dummy_reference, GoogleAutocompleteSubmodule(self.dummy_reference))
            else:
                score.add_score(truth, self.dummy_reference, BingAutocompleteSubmodule(self.dummy_reference))
            gfs.append(GeneratedFact(subject, predicate, obj, "", False, score, MultipleSourceOccurrence()))
        score2 = MultipleScore()
        score2.add_score(1, self.dummy_reference, GoogleAutocompleteSubmodule(self.dummy_reference))
        gfs.append(GeneratedFact("elephant", "be", "big", "", False, score2,
                                 MultipleSourceOccurrence.from_raw("elephants are big", None, 1)))
        inputs = self.empty_input.add_generated_facts(gfs).add_subjects(subjects)
        inputs = sc.process(inputs)
        self.assertEqual(len(dataset) + 1, len(inputs.get_generated_facts()))
        self.assertEqual(len(inputs.get_generated_facts()[0].get_score().scores), 2)
        self.assertNotAlmostEqual(inputs.get_generated_facts()[1].get_score().scores[1][0], 0, delta=1e-5)
