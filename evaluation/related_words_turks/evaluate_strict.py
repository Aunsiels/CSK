import spacy

nlp = spacy.load('en_core_web_sm', disable=["tagger", "parser", "ner"])


def lemmatize(s):
    # return s
    if "has_" in s:
        s = "be"
    doc = nlp(s)
    res = []
    for x in doc:
        res.append(x.lemma_)
    return " ".join(res)


def compute_recall(assos):
    n_assos = 0
    n_found = 0
    with open("turks_data_csk.tsv") as f:
        for line in f:
            line = line.strip().split("\t")
            if line[0] not in assos:
                continue
            # print("SUBJECT", line[0])
            # print("-----------------")
            for sentence in line[1:]:
                sentence = lemmatize(sentence.lower())
                n_assos += len(sentence) - len(line[0])
                maxi = 0
                best = ''
                for relation in assos[line[0]]:
                    if line[0] in relation and len(relation) <= len(
                            line[0]) + 3:
                        continue
                    if relation in sentence:
                        if len(relation) > maxi:
                            maxi = len(relation)
                            best = relation
                n_found += maxi
                # print("For:", sentence, "Best match:", best)
    if n_assos > 0:
        return "%.2f" % (n_found / n_assos * 100) + "%"
    else:
        return 0.0


subjects = set()
with open("subjects.txt") as f:
    for line in f:
        subjects.add(line.strip())

TOPK = 10

def write_top5(basename):
    counts = dict()
    res = []
    with open(basename + ".tsv") as f:
        for line in f:
            subj = line.split("\t")[0]
            if counts.setdefault(subj, 0) >= TOPK:
                continue
            counts[subj] += 1
            res.append(line)
    with open(basename + "_top5.tsv", "w") as f:
        f.write("".join(res))


def read_tsv(path):
    assos = dict()
    with open(path) as f:
        for line in f:
            line = line.strip().split("\t")
            if len(line) < 3:
                continue
            subj = line[0]
            if subj not in subjects:
                continue
            pred = lemmatize(line[1])
            obj = lemmatize(line[2])
            if subj in assos:
                assos[subj].add(pred)
                assos[subj].add(obj)
                assos[subj].add(pred + " " + obj)
            else:
                assos[subj] = {pred, obj}
                assos[subj].add(pred + " " + obj)
    return assos


quasimodo_base = "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37" \
                 "/commonsense_data/quasimodo/quasimodo35_"


for clf in ["lr", "nb", "ada"]:
    basename = quasimodo_base + clf
    write_top5(basename)
    assos = read_tsv(quasimodo_base + clf + "_top5.tsv")
    print("strict top 5 for", clf, compute_recall(assos))


assos = read_tsv("/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37"
                 "/commonsense_data/quasimodo/quasimodo35_lr.tsv")
print("Ours strict", compute_recall(assos))

assos = read_tsv(
    "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/Webchild/webchild_spor.tsv")
print("WebChild strict", compute_recall(assos))

assos = read_tsv(
    "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/ConceptNet/conceptnet_csk_spor.tsv")
print("ConceptNet strict", compute_recall(assos))

assos = read_tsv(
    "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/"
    "TupleKB/aristo-tuple-kb-v5-mar2017/spor_tuplekb.tsv")
print("TupleKB strict", compute_recall(assos))

assos = read_tsv(
    "/home/julien/Documents/phd/CSK/quasimodo/temp/quasimodo34_top5.tsv")
print("Ours strict top5", compute_recall(assos))

assos = read_tsv(
    "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/Webchild/webchild-top5.tsv")
print("WebChild strict top5", compute_recall(assos))

assos = read_tsv(
    "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/ConceptNet/conceptnet_csk_spor_sorted_top5.tsv")
print("ConceptNet strict top5", compute_recall(assos))

assos = read_tsv(
    "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/"
    "TupleKB/aristo-tuple-kb-v5-mar2017/tuplekb-top5.tsv")
print("TupleKB strict top5", compute_recall(assos))
