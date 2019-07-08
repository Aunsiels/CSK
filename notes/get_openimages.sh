#/bin/bash

wget https://storage.googleapis.com/openimages/v5/train-annotations-human-imagelabels.csv
wget https://storage.googleapis.com/openimages/v5/validation-annotations-human-imagelabels.csv
wget https://storage.googleapis.com/openimages/v5/test-annotations-human-imagelabels.csv
wget https://storage.googleapis.com/openimages/v5/train-annotations-machine-imagelabels.csv
wget https://storage.googleapis.com/openimages/v5/validation-annotations-machine-imagelabels.csv
wget https://storage.googleapis.com/openimages/v5/test-annotations-machine-imagelabels.csv
wget https://storage.googleapis.com/openimages/v5/class-descriptions.csv

python3 compute_tags_openimage.py
