from submodule_factory_interface import SubmoduleFactoryInterface
from submodule_google_autocomplete import SubmoduleGoogleAutocomplete
from animal_submodule import AnimalSubmodule
from manual_patterns_google_submodule import ManualPatternsGoogleSubmodule
from bing_autocomplete_submodule import BingAutocompleteSubmodule
from only_subject_submodule import OnlySubjectSubmodule
from no_personal_submodule import NoPersonalSubmodule
from linear_combination_submodule import LinearCombinationSubmodule
from to_singular_subject_submodule import ToSingularSubjectSubmodule
from present_continuous_submodule import PresentContinuousSubmodule
from basic_modality_submodule import BasicModalitySubmodule
from cleaning_predicate_submodule import CleaningPredicateSubmodule
from wikipedia_cooccurrence_submodule import WikipediaCooccurrenceSubmodule
from simple_wikipedia_cooccurrence_submodule import SimpleWikipediaCooccurrenceSubmodule
from antonym_checking_submodule import AntonymCheckingSubmodule
from are_transformation_submodule import AreTransformationSubmodule
from filter_object_submodule import FilterObjectSubmodule
from can_transformation_submodule import CanTransformationSubmodule
from incomplete_modality_submodule import IncompleteModalitySubmodule
from occupations_submodule import OccupationsSubmodule
from conceptnet_subjects_submodule import ConceptnetSubjectsSubmodule


class DefaultSubmoduleFactory(SubmoduleFactoryInterface):
    """DefaultSubmoduleFactory
    The default submodule factory
    """

    def get_submodule(self, submodule_name, module_reference):
        if submodule_name == "google-autocomplete":
            return SubmoduleGoogleAutocomplete(module_reference)
        elif submodule_name == "animal-seeds":
            return AnimalSubmodule(module_reference)
        elif submodule_name == "manual-patterns-google":
            return ManualPatternsGoogleSubmodule(module_reference)
        elif submodule_name == "bing-autocomplete":
            return BingAutocompleteSubmodule(module_reference)
        elif submodule_name == "only-subject":
            return OnlySubjectSubmodule(module_reference)
        elif submodule_name == "no-personal":
            return NoPersonalSubmodule(module_reference)
        elif submodule_name == "linear-combination":
            return LinearCombinationSubmodule(module_reference)
        elif submodule_name == "singular-subject":
            return ToSingularSubjectSubmodule(module_reference)
        elif submodule_name == "present-continuous":
            return PresentContinuousSubmodule(module_reference)
        elif submodule_name == "basic-modality":
            return BasicModalitySubmodule(module_reference)
        elif submodule_name == "cleaning-predicate":
            return CleaningPredicateSubmodule(module_reference)
        elif submodule_name == "wikipedia-cooccurrence":
            return WikipediaCooccurrenceSubmodule(module_reference)
        elif submodule_name == "simple-wikipedia-cooccurrence":
            return SimpleWikipediaCooccurrenceSubmodule(module_reference)
        elif submodule_name == "antonym-checking":
            return AntonymCheckingSubmodule(module_reference)
        elif submodule_name == "are-transformation":
            return AreTransformationSubmodule(module_reference)
        elif submodule_name == "filter-object":
            return FilterObjectSubmodule(module_reference)
        elif submodule_name == "can-transformation":
            return CanTransformationSubmodule(module_reference)
        elif submodule_name == "incomplete-modality":
            return IncompleteModalitySubmodule(module_reference)
        elif submodule_name == "occupations-seeds":
            return OccupationsSubmodule(module_reference)
        elif submodule_name == "conceptnet-subjects":
            return ConceptnetSubjectsSubmodule(module_reference)
        else:
            raise NotImplementedError
