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
    with open("related_words.tsv") as f:
        for line in f:
            line = line.strip().split("\t")
            if line[0] not in assos:
                continue
            n_assos += len(line) - 1
            for word in line[1:]:
                word = lemmatize(word)
                for relation in assos[line[0]]:
                    if word in relation.split(" "):
                        n_found += 1
                        break
    if n_assos > 0:
        return "%.2f" % (n_found / n_assos * 100) + "%"
    else:
        return 0.0

subjects = set()
with open("subjects.txt") as f:
    for line in f:
        subjects.add(line.strip())

assos = dict()
with open("/home/julien/Documents/phd/CSK/quasimodo/temp/quasimodo21.tsv") as f:
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
        else:
            assos[subj] = {pred, obj}

print("Ours relaxed", compute_recall(assos))

assos = dict()
with open("/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/Webchild/webchild_spor.tsv") as f:
    for line in f:
        line = line.strip().split("\t")
        subj = line[0]
        if subj not in subjects:
            continue
        pred = lemmatize(line[1])
        obj = lemmatize(line[2])
        if subj in assos:
            assos[subj].add(pred)
            assos[subj].add(obj)
        else:
            assos[subj] = {pred, obj}

print("WebChild relaxed", compute_recall(assos))

assos = dict()
with open("/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/ConceptNet/conceptnet_csk_spor.tsv") as f:
    for line in f:
        line = line.strip().split("\t")
        subj = line[0]
        if subj not in subjects:
            continue
        pred = lemmatize(line[1])
        obj = lemmatize(line[2])
        if subj in assos:
            assos[subj].add(pred)
            assos[subj].add(obj)
        else:
            assos[subj] = {pred, obj}

print("ConceptNet relaxed", compute_recall(assos))

assos = dict()
with open("/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/"
          "TupleKB/aristo-tuple-kb-v5-mar2017/spor_tuplekb.tsv") as f:
    for line in f:
        line = line.strip().split("\t")
        subj = line[0]
        if subj not in subjects:
            continue
        pred = lemmatize(line[1])
        obj = lemmatize(line[2])
        if subj in assos:
            assos[subj].add(pred)
            assos[subj].add(obj)
        else:
            assos[subj] = {pred, obj}

print("TupleKB relaxed", compute_recall(assos))

assos = dict()
with open("/home/julien/Documents/phd/CSK/quasimodo/temp/quasimodo21_top5.tsv") as f:
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
        else:
            assos[subj] = {pred, obj}

print("Ours top relaxed", compute_recall(assos))

assos = dict()
with open("/home/julien/Documents/phd/CSK/quasimodo/temp/quasimodo21-multiscore-sorted_tau_top5.tsv") as f:
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
        else:
            assos[subj] = {pred, obj}

print("Ours tau top relaxed", compute_recall(assos))

assos = dict()
with open("/home/julien/Documents/phd/CSK/quasimodo/temp/quasimodo21-multiscore-sorted_sigma_top5.tsv") as f:
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
        else:
            assos[subj] = {pred, obj}

print("Ours sigma top relaxed", compute_recall(assos))

assos = dict()
with open("/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/Webchild/webchild-top5.tsv") as f:
    for line in f:
        line = line.strip().split("\t")
        subj = line[0]
        if subj not in subjects:
            continue
        pred = lemmatize(line[1])
        obj = lemmatize(line[2])
        if subj in assos:
            assos[subj].add(pred)
            assos[subj].add(obj)
        else:
            assos[subj] = {pred, obj}

print("WebChild top relaxed", compute_recall(assos))

assos = dict()
with open("/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/ConceptNet/conceptnet-top5.tsv") as f:
    for line in f:
        line = line.strip().split("\t")
        subj = line[0]
        if subj not in subjects:
            continue
        pred = lemmatize(line[1])
        obj = lemmatize(line[2])
        if subj in assos:
            assos[subj].add(pred)
            assos[subj].add(obj)
        else:
            assos[subj] = {pred, obj}

print("ConceptNet top relaxed", compute_recall(assos))

assos = dict()
with open("/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/"
          "TupleKB/aristo-tuple-kb-v5-mar2017/tuplekb-top5.tsv") as f:
    for line in f:
        line = line.strip().split("\t")
        subj = line[0]
        if subj not in subjects:
            continue
        pred = lemmatize(line[1])
        obj = lemmatize(line[2])
        if subj in assos:
            assos[subj].add(pred)
            assos[subj].add(obj)
        else:
            assos[subj] = {pred, obj}

print("TupleKB top relaxed", compute_recall(assos))
