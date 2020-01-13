import unittest

from quasimodo.flickr_clusters_submodule import FlickrClustersSubmodule
from quasimodo.generated_fact import GeneratedFact
from quasimodo.imagetag_submodule import ImagetagSubmodule
from quasimodo.inputs import Inputs
from quasimodo.multiple_scores import MultipleScore
from quasimodo.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.openie_fact_generator_submodule import OpenIEFactGeneratorSubmodule
from quasimodo.referencable_interface import ReferencableInterface
from quasimodo.subject import Subject


class TestAssociation(unittest.TestCase):

    def setUp(self) -> None:
        dummy_reference = ReferencableInterface("Dummy reference")
        self.openie_fact_generator = OpenIEFactGeneratorSubmodule(dummy_reference)
        self.openie_fact_generator._name = "OPENIE"  # Dummy name only useful for testing
        self.empty_input = Inputs()
        self.associations = ImagetagSubmodule(None)
        self.associations_flick_cluster = FlickrClustersSubmodule(None)

    def test_panda_imagetag(self):
        new_gfs = [GeneratedFact("panda", "climb", "tree", "", False, MultipleScore(), MultipleSourceOccurrence())]
        inputs = self.empty_input.add_generated_facts(new_gfs).add_subjects({"panda"})
        inputs = self.associations.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        scores = inputs.get_generated_facts()[0].get_score()
        scores_imagetag = [x for x in scores.scores if x[2].get_name() == "Image Tag submodule"]
        self.assertEqual(1, len(scores_imagetag))

    def test_panda_flickr_cluster(self):
        new_gfs = [GeneratedFact("panda", "live", "china", "", False, MultipleScore(), MultipleSourceOccurrence())]
        inputs = self.empty_input.add_generated_facts(new_gfs).add_subjects({Subject("panda")})
        inputs = self.associations_flick_cluster.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        scores = inputs.get_generated_facts()[0].get_score()
        scores_flickr = [x for x in scores.scores if x[2].get_name() == "Flickr"]
        self.assertEqual(1, len(scores_flickr))

    def test_panda_flickr_cluster_raw(self):
        clusters = self.associations_flick_cluster._get_clusters("panda")
        merge_clusters = []
        for cluster in clusters:
            merge_clusters += cluster
        self.assertIn("china", merge_clusters)


if __name__ == '__main__':
    unittest.main()
