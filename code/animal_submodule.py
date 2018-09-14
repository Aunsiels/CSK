from submodule_interface import SubmoduleInterface
from subject import Subject
from inputs import Inputs

# A file containing a list of animals
filename = "data/anitemp.txt"

class AnimalSubmodule(SubmoduleInterface):
    """AnimalSubmodule
    A submodule to produce animals of the subjects of the input
    """

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Animal Seeds"

    def process(self, input_interface):
        subjects = []
        # Read the subjects from a file
        with open(filename) as f:
            for line in f:
                subjects.append(Subject(line.strip()))
        return input_interface.add_subjects(subjects)
