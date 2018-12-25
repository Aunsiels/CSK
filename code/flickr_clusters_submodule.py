from association_submodule import AssociationSubmodule
import flickr_api
import logging
import os

filename = "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/assos_flickr_clusters.tsv"

class FlickrClustersSubmodule(AssociationSubmodule):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Flickr"

    def _get_clusters(self, subject):
        clusters = []
        try:
            clusters = flickr_api.Tag.getClusters(tag=subject)
        except flickr_api.flickrerrors.FlickrAPIError:
            logging.info(subject + " has no cluster")
        res = []
        for cluster in clusters:
            temp = []
            for tag in cluster.tags:
                temp.append(tag.text.lower())
            res.append(temp)
        return res

    def _get_assos(self, subjects):
        d = dict()
        s_found = set()
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
            subject = subject.get()
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
