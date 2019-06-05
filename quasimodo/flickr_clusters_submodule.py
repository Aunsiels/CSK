from quasimodo.parameters_reader import ParametersReader
from .association_submodule import AssociationSubmodule
import flickr_api
import logging
import os

parameters_reader = ParametersReader()
filename = parameters_reader.get_parameter("flickr-clusters") or ""


class FlickrClustersSubmodule(AssociationSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._module_reference = module_reference
        self._name = "Flickr"

    def _get_clusters(self, subject):
        clusters = []
        try:
            clusters = flickr_api.Tag.getClusters(tag=subject)
        except flickr_api.flickrerrors.FlickrAPIError:
            logging.info(subject + " has no cluster")
        except TypeError:
            logging.info("Problem of type with " + subject)
        res = []
        for cluster in clusters:
            temp = []
            for tag in cluster.tags:
                temp.append(tag.text.lower())
            res.append(temp)
        return res

    def _get_associations(self, subjects):
        d = dict()
        s_found = set()
        subjects = set([x.get() for x in subjects])
        if os.path.isfile(filename):
            with open(filename) as f:
                for line in f:
                    line = line.strip().lower().split("\t")
                    subj = line[0]
                    s_found.add(subj)
                    if subj not in subjects:
                        continue
                    for s in line[1:]:
                        if s == subj:
                            continue
                        if subj in d:
                            d[subj][s] = d[subj].setdefault(s, 0) + 1
                        else:
                            d[subj] = dict()
                            d[subj][s] = 1
        for subject in subjects:
            res = []
            if subject not in s_found:
                clusters = self._get_clusters(subject)
                if len(clusters) == 0:
                    res.append(subject)
                for cluster in clusters:
                    res.append(subject + "\t" + "\t".join(cluster))
                    for s in cluster:
                        if s == subject:
                            continue
                        if subject in d:
                            d[subject][s] = d[subject].setdefault(s, 0) + 1
                        else:
                            d[subject] = dict()
                            d[subject][s] = 1
                with open(filename, "a") as f:
                    f.write("\n".join(res) + "\n")
        return d
