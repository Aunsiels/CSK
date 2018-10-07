class EvaluatorFactoryInterface(object):

    def __init__(self):
        pass

    def get_evaluator(evaluator_name):
        """get_evaluator
        Returns the evaluator associated with a name
        :param evaluator_name: the name of the evaluator
        :type evaluator_name: str
        :return: an evaluator
        :rtype: EvaluatorInterface
        """
        raise NotImplementedError
