class ModuleFactoryInterface(object):
    """ModuleFactoryInterface
    Creates modules
    """

    def get_module(self, module_name):
        """get_module
        Returns a module given a name
        :param module_name: The name of the module
        :type module_name: str
        :return: A module
        :rtype: ModuleInterface
        """
        raise NotImplementedError
