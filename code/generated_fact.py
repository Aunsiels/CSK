from generated_fact_interface import GeneratedFactInterface
from subject import Subject
from object import Object
from predicate import Predicate
from modality import Modality
from fact import Fact

class GeneratedFact(GeneratedFactInterface):
    """GeneratedFact
    The default implementation of GeneratedFactInterface
    """

    def __init__(self,
                 subject,
                 predicate,
                 obj,
                 modality,
                 negative,
                 score,
                 sentence_source,
                 module_source,
                 submodule_source,
                 pattern=None):
        if type(subject) == str:
            self._subject = Subject(subject)
        else:
            self._subject = subject # SubjectInterface
        if type(predicate) == str:
            self._predicate = Predicate(predicate)
        else:
            self._predicate = predicate # PredicateInterface
        if type(obj) == str:
            self._object = Object(obj)
        else:
            self._object = obj # ObjectInterface
        if type(modality) == str:
            self._modality = Modality(modality)
        else:
            self._modality = modality # Optinal ModalityInterface
        self._negative = negative
        self._score = score
        self._sentence_source = sentence_source
        self._module_source = module_source
        self._submodule_source = submodule_source
        self._pattern = pattern

    def get_fact(self):
        return Fact(self.get_subject(),
                    self.get_predicate(),
                    self.get_object(),
                    self.is_negative(),
                    self.get_modality())

    def change_subject(self, new_subject):
        return GeneratedFact(new_subject,
                             self.get_predicate(),
                             self.get_object(),
                             self.get_modality(),
                             self.is_negative(),
                             self.get_score(),
                             self.get_sentence_source(),
                             self.get_module_source(),
                             self.get_submodule_source(),
                             self.get_pattern())

    def change_predicate(self, new_predicate):
        return GeneratedFact(self.get_subject(),
                             new_predicate,
                             self.get_object(),
                             self.get_modality(),
                             self.is_negative(),
                             self.get_score(),
                             self.get_sentence_source(),
                             self.get_module_source(),
                             self.get_submodule_source(),
                             self.get_pattern())

    def change_object(self, new_object):
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             new_object,
                             self.get_modality(),
                             self.is_negative(),
                             self.get_score(),
                             self.get_sentence_source(),
                             self.get_module_source(),
                             self.get_submodule_source(),
                             self.get_pattern())

    def change_modality(self, new_modality):
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             self.get_object(),
                             new_modality,
                             self.is_negative(),
                             self.get_score(),
                             self.get_sentence_source(),
                             self.get_module_source(),
                             self.get_submodule_source(),
                             self.get_pattern())

    def change_score(self, new_score):
        """change_score
        Change the score of the generated fact
        :param new_score: the new score to put
        :type new_score: Float
        :return: A generated fact with the new score
        :rtype: GeneratedFactInterface
        """
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             self.get_object(),
                             self.get_modality(),
                             self.is_negative(),
                             new_score,
                             self.get_sentence_source(),
                             self.get_module_source(),
                             self.get_submodule_source(),
                             self.get_pattern())

    def change_module_source(self, new_module_source):
        """change_module_source
        Change the source module
        :param new_module_source: The new source module reference
        :type new_module_source: ModuleReferenceInterface
        :return: A new generated fact with the new module source
        :rtype: GeneratedFactInterface
        """
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             self.get_object(),
                             self.get_modality(),
                             self.is_negative(),
                             self.get_score(),
                             self.get_sentence_source(),
                             new_module_source,
                             self.get_submodule_source(),
                             self.get_pattern())

    def change_submodule_source(self, new_submodule_source):
        """change_submodule_source
        Change the source submodule
        :param new_submodule_source: The new source submodule reference
        :type new_submodule_source: SubmoduleReferenceInterface
        :return: A new generated fact with the new submodule source
        :rtype: GeneratedFactInterface
        """
        return GeneratedFact(self.get_subject(),
                             self.get_predicate(),
                             self.get_object(),
                             self.get_modality(),
                             self.is_negative(),
                             self.get_score(),
                             self.get_sentence_source(),
                             self.get_module_source(),
                             new_submodule_source,
                             self.get_pattern())
