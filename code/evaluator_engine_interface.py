class EvaluatorEngineInterface(object):

    def __init__(self, evaluator_names):
        """__init__

        :param evaluator_names: The names of the evaluators
        :type evaluator_names: List[String]
        """
        self._evaluators = None  # List[EvaluatorInterface]
        self._evaluator_factory = None  # EvaluatorFactoryInterface
        self._evaluator_names = evaluator_names
        self._setup_evaluators()

    def _setup_evaluators(self):
        if self._evaluator_factory is None:
            raise ValueError("The evaluator factory is not defined")
        self._evaluators = []
        for evaluator in self._evaluator_names:
            self._evaluators.append(
                self._evaluator_factory.get_evaluator(evaluator))

    def get_all_evaluations(self, generated_facts):
        """get_all_evaluations
        Get all the evaluations possible
        :param generated_facts: The facts to evaluate
        :type generated_facts: List[GeneratedFactInterface]
        :return: The names of the evaluator with its score associated
        :rtype: List[(str, float)]
        """
        return [(evaluator.get_name(), evaluator.evaluate(generated_facts))
                for evaluator in self._evaluators]

    def print_evaluation(self, generated_facts):
        """print_evaluation
        Print the results of the evaluations
        :param generated_facts: The facts to evaluate
        :type generated_facts: List[GeneratedFactInterface]
        :return: Nothing
        """
        evaluations = self.get_all_evaluations(generated_facts)
        print("\n".join([x[0] + ": " + str(x[1]) for x in evaluations]))
