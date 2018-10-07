from referencable_interface import ReferencableInterface


class EvaluatorInterface(ReferencableInterface):

    def __init__(self):
        self._name = ""

    def evaluate(self, generated_facts):
        """evaluate
        Evaluate generated facts
        :param generated_facts: the facts generated
        :type generated_facts: List[GeneratedFactInterface]
        :return: the score of the output
        :rtype: float
        """
        raise NotImplementedError
