import logging
import unittest

from quasimodo.data_structures.inputs import Inputs
from quasimodo.default_module_factory import DefaultModuleFactory
from quasimodo.data_structures.subject import Subject
from quasimodo.data_structures.workflow_interface import WorkflowInterface


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='log_testing.txt',
                    filemode='a')


class TestComplete(unittest.TestCase):

    def test_all_workflow(self):
        workflow = TestWorkflow()
        inputs = workflow.generate_input()
        inputs = workflow.run(inputs)
        generated_facts = inputs.get_generated_facts()
        print("\n".join(map(str,generated_facts)))
        self.assertTrue(len(generated_facts) > 0)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    unittest.main()


class TestWorkflow(WorkflowInterface):
    """DefaultWorkflow
    The default workflow used
    """

    def __init__(self):
        module_names = ["patterns",
                        "pattern-fusion",
                        "assertion-generation",
                        "assertion-normalization",
                        "assertion-validation",]
                        #"assertion-fusion"]
        super(TestWorkflow, self).__init__(module_names, DefaultModuleFactory())

    def generate_input(self):
        # just give an empty input to the seed module
        empty_input = Inputs()
        return empty_input.add_subjects({Subject("elephant")})
