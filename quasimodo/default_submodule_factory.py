from quasimodo.assertion_validation.conceptual_captions_comparator_submodule import ConceptualCaptionsComparatorSubmodule
from quasimodo.seeds.forgotten_subjects_submodule import ForgottenSubjectsSubmodule
from quasimodo.assertion_normalization.present_conjugate_normalization import PresentConjugateNormalization
from quasimodo.assertion_output.saliency_and_typicality_computation_submodule import SaliencyAndTypicalityComputationSubmodule
from quasimodo.assertion_output.statistics import StatisticsSubmodule
from quasimodo.assertion_normalization.tbc_cleaner import TBCCleaner
from quasimodo.assertion_output.tsv_output_submodule import TSVOutputSubmodule
from quasimodo.assertion_validation.what_questions_comparator_submodule import WhatQuestionsComparatorSubmodule
from quasimodo.data_structures.submodule_factory_interface import SubmoduleFactoryInterface
from quasimodo.assertion_generation.google_autocomplete_submodule import GoogleAutocompleteSubmodule
from quasimodo.seeds.animal_submodule import AnimalSubmodule
from quasimodo.patterns.manual_patterns_google_submodule import ManualPatternsGoogleSubmodule
from quasimodo.assertion_generation.bing_autocomplete_submodule import BingAutocompleteSubmodule
from quasimodo.assertion_normalization.only_subject_submodule import OnlySubjectSubmodule
from quasimodo.assertion_normalization.no_personal_submodule import NoPersonalSubmodule
from quasimodo.assertion_fusion.linear_combination_submodule import LinearCombinationSubmodule
from quasimodo.assertion_fusion.linear_combination_weighted_submodule import LinearCombinationWeightedSubmodule
from quasimodo.assertion_normalization.to_singular_subject_submodule import ToSingularSubjectSubmodule
from quasimodo.assertion_normalization.present_continuous_submodule import PresentContinuousSubmodule
from quasimodo.assertion_normalization.basic_modality_submodule import BasicModalitySubmodule
from quasimodo.assertion_normalization.cleaning_predicate_submodule import CleaningPredicateSubmodule
from quasimodo.assertion_validation.wikipedia_cooccurrence_submodule import WikipediaCooccurrenceSubmodule
from quasimodo.assertion_validation.simple_wikipedia_cooccurrence_submodule import SimpleWikipediaCooccurrenceSubmodule
from quasimodo.assertion_normalization.antonym_checking_submodule import AntonymCheckingSubmodule
from quasimodo.assertion_normalization.are_transformation_submodule import AreTransformationSubmodule
from quasimodo.assertion_normalization.filter_object_submodule import FilterObjectSubmodule
from quasimodo.assertion_normalization.can_transformation_submodule import CanTransformationSubmodule
from quasimodo.assertion_normalization.incomplete_modality_submodule import IncompleteModalitySubmodule
from quasimodo.seeds.occupations_submodule import OccupationsSubmodule
from quasimodo.seeds.conceptnet_subjects_submodule import ConceptnetSubjectsSubmodule
from quasimodo.assertion_normalization.be_normalization_submodule import BeNormalizationSubmodule
from quasimodo.assertion_generation.reddit_questions_submodule import RedditQuestionsSubmodule
from quasimodo.seeds.conceptnet_seeds_submodule import ConceptNetSeedsSubmodule
from quasimodo.assertion_generation.quora_questions_submodule import QuoraQuestionsSubmodule
from quasimodo.assertion_generation.answerscom_questions_submodule import AnswerscomQuestionsSubmodule
from quasimodo.assertion_validation.imagetag_submodule import ImagetagSubmodule
from quasimodo.assertion_validation.flickr_clusters_submodule import FlickrClustersSubmodule
from quasimodo.assertion_validation.google_book_submodule import GoogleBookSubmodule
from quasimodo.web_search.web_count_submodule import WebCountSubmodule
from quasimodo.web_search.web_regression_submodule import WebRegressionSubmodule
from quasimodo.web_search.youtube_count_submodule import YoutubeCountSubmodule
from quasimodo.web_search.youtube_regression_submodule import YoutubeRegressionSubmodule
from quasimodo.web_search.flickr_count_submodule import FlickrCountSubmodule
from quasimodo.web_search.flickr_regression_submodule import FlickrRegressionSubmodule
from quasimodo.web_search.pinterest_count_submodule import PinterestCountSubmodule
from quasimodo.web_search.pinterest_regression_submodule import PinterestRegressionSubmodule
from quasimodo.web_search.istockphoto_count_submodule import IstockphotoCountSubmodule
from quasimodo.web_search.istockphoto_regression_submodule import IstockphotoRegressionSubmodule
from quasimodo.seeds.subjects_wordnet_submodule import SubjectsWordnetSubmodule
from quasimodo.assertion_generation.yahoo_questions_submodule import YahooQuestionsSubmodule
from quasimodo.assertion_normalization.subject_removal_submodule import SubjectRemovalSubmodule
from quasimodo.assertion_normalization.to_lower_case_submodule import ToLowerCaseSubmodule
from .assertion_normalization.clean_subject import CleanSubject
from .assertion_normalization.filter_language_questions import \
    FilterLanguageQuestions
from .assertion_normalization.similar_object_remover import SimilarObjectRemover
from .assertion_output.circle_saliency import CircleSaliency
from .assertion_validation.perplexity_submodule import PerplexitySubmodule
from .fact_combinor import FactCombinor
from quasimodo.assertion_normalization.identical_subject_object_submodule import IdenticalSubjectObjectSubmodule
from .seeds.special_subjects import SpecialSubjects


class DefaultSubmoduleFactory(SubmoduleFactoryInterface):
    """DefaultSubmoduleFactory
    The default submodule factory
    """

    def __init__(self):
        self._submodules = {
            "google-autocomplete": GoogleAutocompleteSubmodule,
            "animal-seeds": AnimalSubmodule,
            "manual-patterns-google": ManualPatternsGoogleSubmodule,
            "bing-autocomplete": BingAutocompleteSubmodule,
            "only-subject": OnlySubjectSubmodule,
            "no-personal": NoPersonalSubmodule,
            "linear-combination": LinearCombinationSubmodule,
            "linear-combination-weighted": LinearCombinationWeightedSubmodule,
            "singular-subject": ToSingularSubjectSubmodule,
            "present-continuous": PresentContinuousSubmodule,
            "basic-modality": BasicModalitySubmodule,
            "cleaning-predicate": CleaningPredicateSubmodule,
            "wikipedia-cooccurrence": WikipediaCooccurrenceSubmodule,
            "simple-wikipedia-cooccurrence": SimpleWikipediaCooccurrenceSubmodule,
            "antonym-checking": AntonymCheckingSubmodule,
            "are-transformation": AreTransformationSubmodule,
            "filter-object": FilterObjectSubmodule,
            "can-transformation": CanTransformationSubmodule,
            "incomplete-modality": IncompleteModalitySubmodule,
            "occupations-seeds": OccupationsSubmodule,
            "conceptnet-subjects": ConceptnetSubjectsSubmodule,
            "be-normalization": BeNormalizationSubmodule,
            "reddit-questions": RedditQuestionsSubmodule,
            "quora-questions": QuoraQuestionsSubmodule,
            "conceptnet-seeds": ConceptNetSeedsSubmodule,
            "answerscom-questions": AnswerscomQuestionsSubmodule,
            "imagetag": ImagetagSubmodule,
            "flickr-clusters": FlickrClustersSubmodule,
            "google-book": GoogleBookSubmodule,
            "web-count": WebCountSubmodule,
            "web-regression": WebRegressionSubmodule,
            "youtube-count": YoutubeCountSubmodule,
            "youtube-regression": YoutubeRegressionSubmodule,
            "flickr-count": FlickrCountSubmodule,
            "flickr-regression": FlickrRegressionSubmodule,
            "pinterest-count": PinterestCountSubmodule,
            "pinterest-regression": PinterestRegressionSubmodule,
            "istockphoto-count": IstockphotoCountSubmodule,
            "istockphoto-regression": IstockphotoRegressionSubmodule,
            "subjects-wordnet": SubjectsWordnetSubmodule,
            "yahoo-questions": YahooQuestionsSubmodule,
            "subject-removal": SubjectRemovalSubmodule,
            "lower-case": ToLowerCaseSubmodule,
            "fact-combinor": FactCombinor,
            "identical-subj-obj": IdenticalSubjectObjectSubmodule,
            "conceptual-captions": ConceptualCaptionsComparatorSubmodule,
            "tbc-cleaner": TBCCleaner,
            "tsv-output": TSVOutputSubmodule,
            "present-conjugate": PresentConjugateNormalization,
            "statistics": StatisticsSubmodule,
            "what-questions": WhatQuestionsComparatorSubmodule,
            "forgotten-subjects": ForgottenSubjectsSubmodule,
            "saliency-typicality": SaliencyAndTypicalityComputationSubmodule,
            "similar-object-remover": SimilarObjectRemover,
            "circle-saliency": CircleSaliency,
            "filter-language-questions": FilterLanguageQuestions,
            "clean-subject": CleanSubject,
            "special-subjects": SpecialSubjects,
            "perplexity": PerplexitySubmodule
        }

    def get_submodule(self, submodule_name, module_reference):
        if submodule_name in self._submodules:
            return self._submodules[submodule_name](module_reference)
        else:
            raise NotImplementedError
