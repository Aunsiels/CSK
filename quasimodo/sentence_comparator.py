import re
import logging

from quasimodo.content_comparator import ContentComparator
from quasimodo.only_subject_submodule import get_subjects_in_all_forms


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
        logging.info("Reading sentence file...")
        with open(self.filename) as f:
            sentences = f.read()
        logging.info("Start finding subjects")
        for subject in subjects:
            original = variations[subject]
            if original not in self.per_subject:
                self.per_subject[original] = set()
            regex = re.compile("(^|\n)[^\n]*" + subject + "[^\n]*(\n|$)")
            for match in regex.finditer(sentences):
                self.per_subject[original].add(match.group().strip())
        logging.info("End of preprocessing")

    def get_contents(self, subject):
        if len(self.filename) == 0:
            return []
        return self.per_subject.get(subject, [])
