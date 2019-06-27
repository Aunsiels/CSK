# QUASIMODO

QUASIMODO is a system to extract commonsense knowledge from query logs and QA forums.

This is the fruit of a collaboration between Telecom Paris and the Max Planck Institute.

## Citing QUASIMODO

```
@misc{romero2019commonsense,
    title={Commonsense Properties from Query Logs and Question Answering Forums},
    author={Julien Romero and Simon Razniewski and Koninika Pal and Jeff Z. Pan and Archit Sakhadeo and Gerhard Weikum},
    year={2019},
    eprint={1905.10989},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

The paper can be found on [Arxiv](https://arxiv.org/pdf/1905.10989.pdf).

A presentation and data can be found on [D5 website](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/commonsense/quasimodo/).

## Usage

To run the extraction pipeline, run:

```bash
export PYTHONPATH=$PYTHONPATH:`pwd`
cd quasimodo
python3 main.py [parameters.tsv]
```

parameters.tsv is configuration file. You can find a template called parameters\_empty.tsv. Complete it and pass before you start the program and pass it to main.py.

The fields are:

- bing-key: The key to access to bing autocomplete API
- google-book-key: The key to access to Google Book API
- openie-file: A file containing extractions from OPENIE5
- default-mongodb-location: The location of the MongoDB database
- conceptnet-seeds: Subjects extracted from ConceptNet
- flickr-clusters: File which will contains the found flickr-cluster
- imagetag-associations: A file containing the associations from OpenImage
- pattern-first: If true, loop over patterns first. Otherwise, loop over subjects
- out-dir: A file where intermediate and final results are saved
- question-cache-dir: A directory where the transformation from question to statement is saved
- conceptual-caption-file: A file containing the captions from the Conceptual Caption Dataset


## References

### Bing Autocomplete API

[https://azure.microsoft.com/en-us/services/cognitive-services/autosuggest/](https://azure.microsoft.com/en-us/services/cognitive-services/autosuggest/)

### Google Book API

[https://developers.google.com/books/](https://developers.google.com/books/)

### OpenIE5

For now, this is not automatic. A file is outputed in quasimodo/data/, you need to pass it to OPENIE5.

[https://github.com/dair-iitd/OpenIE-standalone](https://github.com/dair-iitd/OpenIE-standalone)

### MongoDB

[https://www.mongodb.com/fr](https://www.mongodb.com/fr)

It is possible to save directly into a file by using a FileCache object, but this is not completly integrated for now.

### ConceptNet

[http://conceptnet.io/](http://conceptnet.io/)

### Flickr API

[https://www.flickr.com/services/api/](https://www.flickr.com/services/api/)

### OpenImage

[https://storage.googleapis.com/openimages/web/index.html](https://storage.googleapis.com/openimages/web/index.html)

A script is given to download and prepare the files.

```bash
cd notes
bash get_openimages.sh
```

### Conceptual Captions

Conceptual captions can be downloaded at [https://ai.google.com/research/ConceptualCaptions](https://ai.google.com/research/ConceptualCaptions)
The captions must be placed in a single file, containing one caption per line.
