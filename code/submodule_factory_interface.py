class SubmoduleFactortyInterface(object):
    """SubmoduleFactortyInterface
    Creates submodules
    """

    def get_submodule(self, submodule_name):
        """get_submodule
        Returns a submodule given a name
        :param submodule_name: The name of the submodule
        :type submodule_name: str
        :return: A submodule
        :rtype: SubmoduleInterface
        """
        raise NotImplementedError
