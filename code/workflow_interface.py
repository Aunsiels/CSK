import time
import os

out_dir = "out/"

class WorkflowInterface(object):
    """WorkflowInterface
    Represents a workflow, i.e. the sequential processing of the input
    """

    def __init__(self, module_names, module_factory):
        self._module_names = module_names
        self._factory = module_factory
        self._workflow = self.get_workflow()
        if not os.path.exists(out_dir):
                os.makedirs(out_dir)

    def get_workflow(self):
        """get_workflow
        Gives the  workflow
        :return: The list of the modules
        :rtype: List[ModuleInterface]
        """
        workflow = []
        for name in self._module_names:
            workflow.append(self._factory.get_module(name))
        return workflow

    def generate_input(self):
        """generate_input
        Generate the input of the workflow, in general the seeds
        :return: The input for this workflow
        :rtype: InputInterface
        """
        raise NotImplementedError

    def run(self, input_interface, save=False):
        """run
        Do one pass over the workflow
        :param input: the input of the workflow
        :return: the result of the workflow, as an input
        :rtype: InputInterface
        """
        modules = self._workflow
        temp_input = input_interface
        for module in modules:
            temp_input = module.process(temp_input)
            if save:
                temp_input.save(out_dir + "out_" + module.get_name() + "_" +
                                str(int(time.time())))
        return temp_input
