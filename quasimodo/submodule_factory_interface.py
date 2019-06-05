class SubmoduleFactoryInterface(object):
    """SubmoduleFactoryInterface
    Creates submodules
    """

    def get_submodule(self, submodule_name, module_reference):
        """get_submodule
        Returns a submodule given a name
        :param submodule_name: The name of the submodule
        :type submodule_name: str
        :return: A submodule
        :rtype: SubmoduleInterface
        """
        raise NotImplementedError
