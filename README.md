# QUASIMODO

QUASIMODO is a system to extract commonsense knowledge from query logs and QA forums.

This is the fruit of a collaboration between Telecom Paris and the Max Planck Institute.

## Citing QUASIMODO

The paper can be found on [Arxiv](https://arxiv.org/pdf/1905.10989.pdf).

A presentation and **data** can be found on [D5 website](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/commonsense/quasimodo/).

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
- properties-dir: A directory containing files which group categories for hasProperty


## Using the code


The code is composed of many componants which can be reused and extended.

The extraction pipeline is represented as a Workflow, which passes inputs from one module to the next one.

### The inputs

The inputs are represented by the Inputs class. They are generally processed by a module, which will return a new Inputs.

### Workflow

A workflow is represented by the WorkflowInterface class, which needs to be extended. To do so, one needs to implement the method generating the initial input, generate\_input. Then, the constructor needs to pass to the superclass a list of module names and a factory to create these modules. An example of workflow can be found in the DefaultWorkflow class.

### Module

A module takes as input an InputInterface and returns and InputInterface which has received all the transformations of the module.

A module represents a general type of transformation we want to perform. It is composed of several submodules which are the subtasks of the module.

A module is represented by the ModuleInterface class, which needs to be extended. To do so, one needs to implement the process method and, similarly to the Workflow, must define a list of submodules names and a submodule factory which are going to be passed to the superclass constructor (ModuleInterface). An example can be found in AssertionValidationModule.

### Submodule

A submodule is a smallest componant of the workflow. Similarly to the module, it takes as input an InputInterface and returns and InputInterface which has received all the transformations of the submodule.

A submodule is represented by the SubmoduleInterface class, which needs to be extended. To do so, one is required to implement the process method and to define the \_module\_reference attribute and the \_name attribute. An example can be found in BeNormalizationSubmodule.

An useful class to extend is OpenIEFactGeneratorSubmodule, which allows to generate the facts. An example to do so can be found in QuestionFileSubmodule.

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

### Traits

Extracted from [http://ideonomy.mit.edu/essays/traits.html](http://ideonomy.mit.edu/essays/traits.html)

### Colors

Extracted from [https://simple.wikipedia.org/wiki/List_of_colors](https://simple.wikipedia.org/wiki/List_of_colors)

### Movements

Extracted from [https://thedramateacher.com/words-used-to-describe-movement-in-performance/](https://thedramateacher.com/words-used-to-describe-movement-in-performance/)

### Adjectives and Adverbs list

Extracted from [https://www.englishclub.com](https://www.englishclub.com)
