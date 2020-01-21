class ProcessInterface(object):
    """ProcessInterface
    Something that can be processed
    """

    def process(self, input_interface):
        """process
        Do the processing
        :param input_interface: the input to process
        :type input_interface: InputInterface
        :return: the result of the processing
        :rtype: InputInterface
        """
        raise NotImplementedError
