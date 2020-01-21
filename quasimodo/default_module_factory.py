from quasimodo.assertion_output.output_module import OutputModule
from .module_factory_interface import ModuleFactoryInterface
from quasimodo.assertion_generation.assertion_generation_module import AssertionGenerationModule
from quasimodo.seeds.animal_seed_module import AnimalSeedModule
from .pattern_module import PatternModule
from quasimodo.patterns.pattern_fusion_module import PatternFusionModule
from quasimodo.assertion_normalization.assertion_normalization_module import AssertionNormalizationModule
from quasimodo.assertion_validation.assertion_validation_module import AssertionValidationModule
from quasimodo.assertion_fusion.assertion_fusion_module import AssertionFusionModule
from quasimodo.seeds.occupations_seed_module import OccupationsSeedModule
from quasimodo.seeds.all_seeds_module import AllSeedsModule
from quasimodo.web_search.archit_module import ArchitModule


class DefaultModuleFactory(ModuleFactoryInterface):
    """DefaultModuleFactory
    The default module factory
    """

    def get_module(self, module_name):
        if module_name == "assertion-generation":
            return AssertionGenerationModule()
        elif module_name == "animal-seeds":
            return AnimalSeedModule()
        elif module_name == "patterns":
            return PatternModule()
        elif module_name == "pattern-fusion":
            return PatternFusionModule()
        elif module_name == "assertion-normalization":
            return AssertionNormalizationModule()
        elif module_name == "assertion-validation":
            return AssertionValidationModule()
        elif module_name == "assertion-fusion":
            return AssertionFusionModule()
        elif module_name == "occupations-seeds":
            return OccupationsSeedModule()
        elif module_name == "all-seeds":
            return AllSeedsModule()
        elif module_name == "archit":
            return ArchitModule()
        elif module_name == "output":
            return OutputModule()
        raise NotImplementedError
