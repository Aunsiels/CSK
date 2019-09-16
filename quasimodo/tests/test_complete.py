import unittest

from quasimodo.inputs import Inputs
from quasimodo.default_module_factory import DefaultModuleFactory
from quasimodo.subject import Subject
from quasimodo.workflow_interface import WorkflowInterface


class TestComplete(unittest.TestCase):

    def test_all_workflow(self):
        workflow = TestWorkflow()
        inputs = workflow.generate_input()
        inputs = workflow.run(inputs)
        generated_facts = inputs.get_generated_facts()
        print("\n".join(map(str,generated_facts)))
        self.assertTrue(len(generated_facts) > 0)


if __name__ == '__main__':
    unittest.main()


class TestWorkflow(WorkflowInterface):
    """DefaultWorkflow
    The default workflow used
    """

    def __init__(self):
        module_names = ["patterns",
                        "pattern-fusion",
                        "assertion-generation",]
                        #"assertion-normalization",
                        #"assertion-validation",
                        #"assertion-fusion"]
        super(TestWorkflow, self).__init__(module_names, DefaultModuleFactory())

    def generate_input(self):
        # just give an empty input to the seed module
        empty_input = Inputs()
        return empty_input.add_subjects({Subject("elephant")})