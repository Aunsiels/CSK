import logging
import os

import gensim.downloader as api
from gensim import matutils
from nltk.tokenize import word_tokenize
import numpy as np

from quasimodo.parameters_reader import ParametersReader
from quasimodo.submodule_interface import SubmoduleInterface
from quasimodo.tsv_output_submodule import get_version

SLICE_SIZE = 10000  # Change this in case of Memory problems
TOPK = 5


parameters_reader = ParametersReader()
OUT_DIR = parameters_reader.get_parameter("out-dir") or os.path.dirname(__file__) + "/out/"


def save_tsv_triples(triples):
    version = get_version()
    save_file = OUT_DIR + "quasimodo" + str(version) + ".tsv"
    with open(save_file, "w") as f:
        f.write("\t".join(["subject", "predicate", "object", "modality", "is_negative", "score", "sentences source",
                           "typicality", "saliency"]) + "\n")
        f.write("\n".join(triples))


class SaliencyAndTypicalityComputationSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Saliency and typicality"
        self.total_per_subject = dict()
        self.total_per_po = dict()
        self.idx2keys = []
        self.idx2total = []
        self.vectors = None
        self.probabilities_po = None

    def get_all_triples_as_tsv(self, input_interface):
        triples = []
        for generated_fact in input_interface.get_generated_facts():
            row_tsv = generated_fact.get_tsv()
            subj = generated_fact.get_subject().get()
            pred = generated_fact.get_predicate().get()
            obj = generated_fact.get_object().get()
            score = generated_fact.get_score().scores[0][0]
            po = pred + " " + obj
            tau = score / self.total_per_subject[subj]
            sigma = score / self.total_per_po[po]
            triples.append(row_tsv + "\t" + str(tau) + "\t" + str(sigma))
        return triples

    def process(self, input_interface):
        logging.info("Start TSV output submodule")

        self.initialize_statistics(input_interface)
        self.initialize_idx_correspondences()
        self.initialize_po_vectors()
        self.compute_probabilities()
        self.match_probabilities()
        self.save_final_results(input_interface)

        return input_interface

    def save_final_results(self, input_interface):
        triples = self.get_all_triples_as_tsv(input_interface)
        save_tsv_triples(triples)

    def match_probabilities(self):
        for i, key in enumerate(self.idx2keys):
            self.total_per_po[key] = self.probabilities_po[i]

    def compute_probabilities(self):
        self.probabilities_po = np.zeros(self.vectors.shape[0])
        distances_temp = None
        for i in range(self.vectors.shape[0]):
            if i % SLICE_SIZE == 0:
                print(i / self.vectors.shape[0] * 100, end="\r")
                distances_temp = np.dot(self.vectors[i:i + SLICE_SIZE], self.vectors.T)
            idx_closest = matutils.argsort(distances_temp[i % SLICE_SIZE],
                                           topn=TOPK,
                                           reverse=True)
            closest_indexes = [(j, distances_temp[i % SLICE_SIZE][j]) for j in idx_closest]
            norm = sum([x[1] for x in closest_indexes])
            weighted_sum = sum([x[1] * self.idx2total[x[0]] for x in closest_indexes])
            self.probabilities_po[i] = weighted_sum / norm

    def initialize_po_vectors(self):
        model = api.load("word2vec-google-news-300")
        self.vectors = np.zeros((len(self.idx2keys), model.vector_size))
        for i, sentence in enumerate(self.idx2keys):
            sentence = sentence.lower().replace("_", " ")
            sentence = word_tokenize(sentence)
            counter = 0
            for word in sentence:
                if word in model.vocab:
                    self.vectors[i] += model.get_vector(word)
                    counter += 1
            if counter == 0:
                pass
            else:
                self.vectors[i] = self.vectors[i] / counter
        norms = np.sqrt((self.vectors * self.vectors).sum(axis=1)).reshape(self.vectors.shape[0], 1)
        self.vectors /= norms

    def initialize_idx_correspondences(self):
        self.idx2keys = list(self.total_per_po.keys())
        self.idx2total = [self.total_per_po[key] for key in self.idx2keys]

    def initialize_statistics(self, input_interface):
        self.total_per_subject = dict()
        self.total_per_po = dict()
        for generated_fact in input_interface.get_generated_facts():
            subj = generated_fact.get_subject().get()
            pred = generated_fact.get_predicate().get()
            obj = generated_fact.get_object().get()
            score = generated_fact.get_score().scores[0][0]
            self.total_per_subject[subj] = self.total_per_subject.setdefault(subj, 0) + score
            po = pred + " " + obj
            self.total_per_po[po] = self.total_per_po.setdefault(po, 0) + score
