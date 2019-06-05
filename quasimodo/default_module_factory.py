from .module_factory_interface import ModuleFactoryInterface
from .assertion_generation_module import AssertionGenerationModule
from .animal_seed_module import AnimalSeedModule
from .pattern_module import PatternModule
from .pattern_fusion_module import PatternFusionModule
from .assertion_normalization_module import AssertionNormalizationModule
from .assertion_validation_module import AssertionValidationModule
from .assertion_fusion_module import AssertionFusionModule
from .occupations_seed_module import OccupationsSeedModule
from .all_seeds_module import AllSeedsModule
from .archit_module import ArchitModule


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
        raise NotImplementedError
