from quasimodo.content_comparator import ContentComparator
from quasimodo.only_subject_submodule import get_subjects_in_all_forms
from nltk import ngrams


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
        subjects, variations = get_subjects_in_all_forms(input_interface)
        with open(self.filename) as f:
            for line in f:
                new_line = line.strip().split(" ")
                for n in range(1, 5):
                    sub_words = ngrams(new_line, n)
                    for words in sub_words:
                        word = " ".join(words)
                        if word in subjects:
                            subject = variations[word]
                            if subject in self.per_subject:
                                self.per_subject[subject].append(line)
                            else:
                                self.per_subject[subject] = [line]

    def get_contents(self, subject):
        if len(self.filename) == 0:
            return []
        return self.per_subject.get(subject, [])
