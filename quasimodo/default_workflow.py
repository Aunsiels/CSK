from quasimodo.data_structures.workflow_interface import WorkflowInterface
from .default_module_factory import DefaultModuleFactory
from quasimodo.data_structures.inputs import Inputs


class DefaultWorkflow(WorkflowInterface):
    """DefaultWorkflow
    The default workflow used
    """

    def __init__(self):
        module_names = ["patterns",
                        "pattern-fusion",
                        "assertion-generation",
                        "archit",
                        "assertion-normalization",
                        "assertion-validation",
                        "assertion-fusion",
                        "output"]
        super(DefaultWorkflow, self).__init__(
            module_names, DefaultModuleFactory())
        self._seeds = self._factory.get_module("all-seeds")

    def generate_input(self):
        # just give an empty input to the seed module
        return self._seeds.process(Inputs([], [], [], [], []))
