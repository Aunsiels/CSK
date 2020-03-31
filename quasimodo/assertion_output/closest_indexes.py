import numpy as np
from gensim import matutils

SLICE_SIZE = 5000  # Change this in case of Memory problems


class ClosestIndexes:

    def __init__(self, similarities):
        self.vectors = similarities
        # Normalize just in case
        norms = np.sqrt((self.vectors * self.vectors).sum(axis=1)).reshape(
            self.vectors.shape[0], 1)
        self.vectors /= norms

    def get_closest_indexes(self, top_k, slice_size=SLICE_SIZE):
        closest_indexes = []
        similarity_temp = None
        for i in range(self.vectors.shape[0]):
            if i % slice_size == 0:
                similarity_temp = np.dot(self.vectors[i:i + slice_size],
                                         self.vectors.T)
            idx_closest = matutils.argsort(similarity_temp[i % slice_size],
                                           topn=top_k,
                                           reverse=True)
            closest_indexes.append(
                [(j, (1.0 + similarity_temp[i % slice_size][j]) / 2.0)
                 for j in idx_closest])
        return closest_indexes
