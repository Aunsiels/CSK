mkdir perplexity -p

cut -f2 quasimodo/question2statement/cache.tsv | sort -u > perplexity/sentences.txt
cd perplexity

pip3 install -r requirements.txt
python3 preprocess.py
python3 compute_ppl.py 
