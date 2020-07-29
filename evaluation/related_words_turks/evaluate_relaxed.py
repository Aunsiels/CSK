import spacy
nlp = spacy.load('en_core_web_sm', disable=["tagger", "parser", "ner"])


PREDICATES_CONCEPTNET = {
    "AtLocation": "be in",
    "CapableOf": "can",
    "Causes": "cause",
    "CausesDesire": "cause desire",
    "CreatedBy": "create by",
    "DefinedAs": "define as",
    "Desires": "desire",
    "DistinctFrom": "be distinct from",
    "Entails": "entail",
    "HasA": "have",
    "HasFirstSubevent": "have",
    "HasLastSubevent": "have",
    "HasPrerequisite": "need",
    "HasProperty": "be",
    "HasSubevent": "have",
    "InstanceOf": "be",
    "LocatedNear": "be near",
    "MadeOf": "make of",
    "MannerOf": "be",
    "MotivatedByGoal": "motivate by",
    "PartOf": "be part of",
    "ReceivesAction": "receive action",
    "UsedFor": "use for",
    "has_body_part": "be",
    "has_color": "be",
    "has_diet": "be",
    "has_effect": "be",
    "has_height": "be",
    "has_manner": "be",
    "has_movement": "be",
    "has_place": "be",
    "has_property": "be",
    "has_temperature": "be",
    "has_time": "be",
    "has_trait": "be",
    "has_weather": "be",
    "has_weight": "be"
}


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
            pred = line[1]
            if pred in PREDICATES_CONCEPTNET:
                pred = PREDICATES_CONCEPTNET[pred]
            pred = lemmatize(pred)
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


# for clf in ["lr", "nb", "ada"]:
#     basename = quasimodo_base + clf
#     write_top5(basename)
#     assos = read_tsv(quasimodo_base + clf + "_top5.tsv")
#     print("relaxed top", TOPK, "for", clf, compute_recall(assos))
#
# assos = read_tsv("/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37"
#                  "/commonsense_data/quasimodo/quasimodo35_lr.tsv")
# print("Ours relaxed", compute_recall(assos))
#
# assos = read_tsv(
#     "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/Webchild/webchild_spor.tsv")
# print("WebChild relaxed", compute_recall(assos))
#
# assos = read_tsv(
#     "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/ConceptNet/conceptnet_csk_spor.tsv")
# print("ConceptNet relaxed", compute_recall(assos))
#
# assos = read_tsv(
#     "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/"
#     "TupleKB/aristo-tuple-kb-v5-mar2017/spor_tuplekb.tsv")
# print("TupleKB relaxed", compute_recall(assos))
#
write_top5(quasimodo_base + "lr")
assos = read_tsv(quasimodo_base + "lr" + "_top5.tsv")
print("Ours relaxed top", TOPK, compute_recall(assos))
#
# assos = read_tsv(
#     "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/Webchild/webchild-top5.tsv")
# print("WebChild relaxed top", TOPK, compute_recall(assos))
#
# assos = read_tsv(
#     "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/ConceptNet/conceptnet_csk_spor_sorted_top5.tsv")
# print("ConceptNet relaxed top", TOPK, compute_recall(assos))
#
# assos = read_tsv(
#     "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/"
#     "TupleKB/aristo-tuple-kb-v5-mar2017/tuplekb-top5.tsv")
# print("TupleKB relaxed top", TOPK, compute_recall(assos))

def sort_by(basename, n):
    temp = []
    first = True
    with open(basename + ".tsv") as f:
        for line in f:
            if not first:
                temp.append(line.split("\t"))
            first = False
    temp = sorted(temp, key=lambda x: -float(x[n].strip()))
    with open(basename + "_sorted" + str(n) + ".tsv", "w") as f:
        f.write("".join("\t".join(x) for x in temp))

sort_by(quasimodo_base + "lr_pts50", -2)
write_top5(quasimodo_base + "lr_pts50_sorted-2")
assos = read_tsv(quasimodo_base + "lr_pts50_sorted-2_top5.tsv")
print("Typicality top", TOPK, " N=50", compute_recall(assos))

sort_by(quasimodo_base + "lr_pts50", -1)
write_top5(quasimodo_base + "lr_pts50_sorted-1")
assos = read_tsv(quasimodo_base + "lr_pts50_sorted-1_top5.tsv")
print("Saliency top", TOPK, " N=50", compute_recall(assos))

sort_by(quasimodo_base + "lr_pts1", -2)
write_top5(quasimodo_base + "lr_pts1_sorted-2")
assos = read_tsv(quasimodo_base + "lr_pts1_sorted-2_top5.tsv")
print("Typicality top", TOPK, " N=1", compute_recall(assos))

sort_by(quasimodo_base + "lr_pts1", -1)
write_top5(quasimodo_base + "lr_pts1_sorted-1")
assos = read_tsv(quasimodo_base + "lr_pts1_sorted-1_top5.tsv")
print("Saliency top", TOPK, " N=1", compute_recall(assos))

sort_by(quasimodo_base + "lr_pts", -2)
write_top5(quasimodo_base + "lr_pts_sorted-2")
assos = read_tsv(quasimodo_base + "lr_pts_sorted-2_top5.tsv")
print("Typicality top", TOPK, " N=5", compute_recall(assos))

sort_by(quasimodo_base + "lr_pts", -1)
write_top5(quasimodo_base + "lr_pts_sorted-1")
assos = read_tsv(quasimodo_base + "lr_pts_sorted-1_top5.tsv")
print("Saliency top", TOPK, " N=5", compute_recall(assos))

sort_by(quasimodo_base + "lr_pts10", -2)
write_top5(quasimodo_base + "lr_pts10_sorted-2")
assos = read_tsv(quasimodo_base + "lr_pts10_sorted-2_top5.tsv")
print("Typicality top", TOPK, " N=10", compute_recall(assos))

sort_by(quasimodo_base + "lr_pts10", -1)
write_top5(quasimodo_base + "lr_pts10_sorted-1")
assos = read_tsv(quasimodo_base + "lr_pts10_sorted-1_top5.tsv")
print("Saliency top", TOPK, " N=10", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln0.1", -2)
write_top5(quasimodo_base + "lr_ln0.1_sorted-2")
assos = read_tsv(quasimodo_base + "lr_ln0.1_sorted-2_top5.tsv")
print("Neighborhood top", TOPK, "N=0.1", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln0.1", -1)
write_top5(quasimodo_base + "lr_ln0.1_sorted-1")
assos = read_tsv(quasimodo_base + "lr_ln0.1_sorted-1_top5.tsv")
print("Local Neighborhood top", TOPK, "N=0.1", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln0.5", -2)
write_top5(quasimodo_base + "lr_ln0.5_sorted-2")
assos = read_tsv(quasimodo_base + "lr_ln0.5_sorted-2_top5.tsv")
print("Neighborhood top", TOPK, "N=0.5", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln0.5", -1)
write_top5(quasimodo_base + "lr_ln0.5_sorted-1")
assos = read_tsv(quasimodo_base + "lr_ln0.5_sorted-1_top5.tsv")
print("Local Neighborhood top", TOPK, "N=0.5", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln1", -2)
write_top5(quasimodo_base + "lr_ln1_sorted-2")
assos = read_tsv(quasimodo_base + "lr_ln1_sorted-2_top5.tsv")
print("Neighborhood Sigma top", TOPK,  "N=1", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln1", -1)
write_top5(quasimodo_base + "lr_ln1_sorted-1")
assos = read_tsv(quasimodo_base + "lr_ln1_sorted-1_top5.tsv")
print("Local Sigma top", TOPK, "N=1", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln10", -2)
write_top5(quasimodo_base + "lr_ln10_sorted-2")
assos = read_tsv(quasimodo_base + "lr_ln10_sorted-2_top5.tsv")
print("Neighborhood top", TOPK, "N=10", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln10", -1)
write_top5(quasimodo_base + "lr_ln10_sorted-1")
assos = read_tsv(quasimodo_base + "lr_ln10_sorted-1_top5.tsv")
print("Local Neighborhood top", TOPK, "N=10", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln25", -2)
write_top5(quasimodo_base + "lr_ln25_sorted-2")
assos = read_tsv(quasimodo_base + "lr_ln25_sorted-2_top5.tsv")
print("Neighborhood top", TOPK, "N=25", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln25", -1)
write_top5(quasimodo_base + "lr_ln25_sorted-1")
assos = read_tsv(quasimodo_base + "lr_ln25_sorted-1_top5.tsv")
print("Local Neighborhood top", TOPK, "N=25", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln50", -2)
write_top5(quasimodo_base + "lr_ln50_sorted-2")
assos = read_tsv(quasimodo_base + "lr_ln50_sorted-2_top5.tsv")
print("Neighborhood top", TOPK, "N=50", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln50", -1)
write_top5(quasimodo_base + "lr_ln50_sorted-1")
assos = read_tsv(quasimodo_base + "lr_ln50_sorted-1_top5.tsv")
print("Local Neighborhood top", TOPK, "N=50", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln75", -2)
write_top5(quasimodo_base + "lr_ln75_sorted-2")
assos = read_tsv(quasimodo_base + "lr_ln75_sorted-2_top5.tsv")
print("Neighborhood top", TOPK, "N=75", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln75", -1)
write_top5(quasimodo_base + "lr_ln75_sorted-1")
assos = read_tsv(quasimodo_base + "lr_ln75_sorted-1_top5.tsv")
print("Local Neighborhood top", TOPK, "N=75", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln100", -2)
write_top5(quasimodo_base + "lr_ln100_sorted-2")
assos = read_tsv(quasimodo_base + "lr_ln100_sorted-2_top5.tsv")
print("Neighborhood top", TOPK, "N=100", compute_recall(assos))

sort_by(quasimodo_base + "lr_ln100", -1)
write_top5(quasimodo_base + "lr_ln100_sorted-1")
assos = read_tsv(quasimodo_base + "lr_ln100_sorted-1_top5.tsv")
print("Local Neighborhood top", TOPK, "N=100", compute_recall(assos))

