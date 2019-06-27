from quasimodo.content_comparator import ContentComparator


class SentenceComparator(ContentComparator):

    def __init__(self, module_reference, filename):
        super().__init__(module_reference)
        self.filename = filename
        self.per_subject = dict()
        self._name = "Sentence Comparator"

    def setup_processing(self, input_interface):
        if len(self.filename) == 0:
            return
        self.per_subject = dict()
        subjects = input_interface.get_subjects()
        with open(self.filename) as f:
            for line in f:
                line = line.strip()
                for subject in subjects:
                    if subject in subjects:
                        subject = subject.get()
                        if subject in line:
                            if subject in self.per_subject:
                                self.per_subject[subject].append(line)
                            else:
                                self.per_subject[subject] = [line]

    def get_contents(self, subject):
        if len(self.filename) == 0:
            return []
        return self.per_subject.get(subject, "")