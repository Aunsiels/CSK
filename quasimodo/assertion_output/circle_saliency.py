import logging
import os

import gensim.downloader as api
from gensim import matutils
from nltk.tokenize import word_tokenize
import numpy as np

from quasimodo.assertion_output.saliency_and_typicality_computation_submodule import get_raw_predicate
from quasimodo.parameters_reader import ParametersReader
from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.assertion_output.tsv_output_submodule import get_version

SLICE_SIZE = 2000  # Change this in case of Memory problems
TOPK = 1000
N = 1

parameters_reader = ParametersReader()
OUT_DIR = parameters_reader.get_parameter("out-dir") or os.path.dirname(__file__) + "/out/"


def save_tsv_triples(triples):
    version = get_version()
    save_file = OUT_DIR + "quasimodo" + str(version) + ".tsv"
    with open(save_file, "w") as f:
        f.write("\t".join(["subject", "predicate", "object", "modality", "is_negative", "score", "sentences source",
                           "neighborhood sigma", "local sigma"]) + "\n")
        f.write("\n".join(triples))


class CircleSaliency(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Saliency and typicality"
        self.total_per_po = dict()
        self.total_per_po_per_subject = dict()
        self.idx2keys = []
        self.keys2idx = dict()
        self.vectors = None
        self.saliencies = []
        self.closest_indexes = []

    def compute_sigma(self, subj, po, score):
        cum_sum = 0
        sigma = 0
        i = 0
        j = 0
        idx = self.keys2idx[po]
        while cum_sum < score * N and i < TOPK and j < len(self.closest_indexes[idx]):
            current_closest, similarity = self.closest_indexes[idx][j]
            j += 1
            if current_closest == idx:
                continue
            key = self.idx2keys[current_closest]
            non_subj_score = self.total_per_po[key] - self.total_per_po_per_subject.get((subj, key), 0)
            # Ignore po from the subject
            if non_subj_score < 1e-4:
                continue
            cum_sum += non_subj_score * similarity
            sigma = 1 - similarity
            i += 1
        return sigma, score / self.total_per_po[po]

    def get_all_triples_as_tsv(self, input_interface):
        triples = []
        for i, generated_fact in enumerate(input_interface.get_generated_facts()):
            row_tsv = generated_fact.get_tsv()
            neighborhood_sigma, local_sigma = self.saliencies[i]
            triples.append(row_tsv + "\t" + str(neighborhood_sigma) + "\t" + str(local_sigma))
        return triples

    def set_sigmas(self, input_interface):
        self.saliencies = []
        for generated_fact in input_interface.get_generated_facts():
            subj = generated_fact.get_subject().get()
            pred = get_raw_predicate(generated_fact.get_predicate().get())
            obj = generated_fact.get_object().get()
            score = generated_fact.get_score().scores[0][0]
            po = pred + " " + obj
            sigma = self.compute_sigma(subj, po, score)
            self.saliencies.append(sigma)

    def process(self, input_interface):
        logging.info("Start TSV output submodule")

        self.initialize_statistics(input_interface)
        self.initialize_idx_correspondences()
        self.initialize_po_vectors()
        self.set_closest_indexes()
        self.set_sigmas(input_interface)
        self.save_final_results(input_interface)

        return input_interface

    def save_final_results(self, input_interface):
        triples = self.get_all_triples_as_tsv(input_interface)
        save_tsv_triples(triples)

    def set_closest_indexes(self):
        self.closest_indexes = []
        distances_temp = None
        for i in range(self.vectors.shape[0]):
            if i % SLICE_SIZE == 0:
                distances_temp = np.dot(self.vectors[i:i + SLICE_SIZE], self.vectors.T)
            idx_closest = matutils.argsort(distances_temp[i % SLICE_SIZE],
                                           topn=TOPK,
                                           reverse=True)
            self.closest_indexes.append([(j, (1 - distances_temp[i % SLICE_SIZE][j])) for j in idx_closest])
        return self.closest_indexes

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
        for i, key in enumerate(self.total_per_po.keys()):
            self.keys2idx[key] = i

    def initialize_statistics(self, input_interface):
        self.total_per_po = dict()
        self.total_per_po_per_subject = dict()
        for generated_fact in input_interface.get_generated_facts():
            subj = generated_fact.get_subject().get()
            pred = get_raw_predicate(generated_fact.get_predicate().get())
            obj = generated_fact.get_object().get()
            score = generated_fact.get_score().scores[0][0]
            po = pred + " " + obj
            self.total_per_po[po] = self.total_per_po.get(po, 0) + score
            self.total_per_po_per_subject[(subj, po)] = self.total_per_po_per_subject.get((subj, po), 0) + score
