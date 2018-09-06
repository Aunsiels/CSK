class WorkflowInterface(object):
    """WorkflowInterface
    Represents a workflow, i.e. the sequential processing of the input
    """

    def __init__(self):
        self._factory = None

    def get_workflow(self):
        """get_workflow
        Gives the  workflow
        :return: The list of the modules
        :rtype: List[ModuleInterface]
        """
        raise NotImplementedError

    def generate_input(self):
        """generate_input
        Generate the input of the workflow, in general the seeds
        :return: The input for this workflow
        :rtype: InputInterface
        """
        raise NotImplementedError

    def run(self, input_interface):
        """run
        Do one pass over the workflow
        :param input: the input of the workflow
        :return: the result of the workflow, as an input
        :rtype: InputInterface
        """
        modules = self.get_workflow()
        temp_input = input_interface
        for module in modules:
            temp_input = module.process(temp_input)
        return temp_input
