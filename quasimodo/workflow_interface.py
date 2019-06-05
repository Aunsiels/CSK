import time
import os
import logging
import pickle

out_dir = os.path.dirname(__file__) + "/out/"


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
        return self.run_from(input_interface, save, 0)

    def run_from(self, input_interface=None, save=False, idx_from=0):
        modules = self._workflow
        temp_input = input_interface
        if idx_from >= len(modules) or idx_from < 0:
            raise ValueError("The index is incorrect")
        elif idx_from == 0 and input_interface is None:
            input_interface = self.generate_input()
        elif input_interface is None:
            input_interface = self._load_last(modules[idx_from - 1])
        temp_input = input_interface
        for module in modules[idx_from:]:
            logging.info("We have " + str(len(temp_input.get_generated_facts())) + " facts")
            temp_input = module.process(temp_input)
            if save:
                temp_input.save(out_dir + "out_" + str(int(time.time())) + "_" +
                                module.get_name())
        return temp_input

    def _load_last(self, module):
        outs = os.listdir("out/")
        outs = [x for x in outs if module.get_name() in x]
        if outs:
            filename = sorted(outs)[-1]
            with open("out/" + filename, "rb") as f:
                logging.info("Loading " + filename)
                return pickle.loads(f.read())
        return self.generate_input()

    def __str__(self):
        res = []
        res.append("WORKFLOW")
        for module in self._workflow:
            res.append(str(module))
        return "\n".join(res)

    def print_index(self):
        count = 0
        for module in self._workflow:
            print("[", str(count), "]:", module.get_name())
            count += 1
