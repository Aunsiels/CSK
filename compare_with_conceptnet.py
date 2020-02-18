from quasimodo.assertion_output.saliency_and_typicality_computation_submodule import get_raw_predicate
from quasimodo.spacy_accessor import get_default_annotator

QUASIMODO_FILENAME = "/home/julien/Documents/phd/CSK/quasimodo/temp/quasimodo27.tsv"
CONCEPT_NET = "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/ConceptNet/conceptnet_csk_spor.tsv"

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
    "UsedFor": "use for"
}

spacy_annotator = get_default_annotator()

conceptnet_raw = []
with open(CONCEPT_NET) as f:
    for line in f:
        line = line.strip().split("\t")
        line = "\t".join([line[0], PREDICATES_CONCEPTNET[line[1]], line[2]])
        conceptnet_raw.append(line.strip().replace("_", " "))

conceptnet_raw = spacy_annotator.lemmatize_multiple(conceptnet_raw)

print(len(conceptnet_raw), len(conceptnet_raw[0]))
print(conceptnet_raw[0])

conceptnet = dict()
for line in conceptnet_raw:
    line = [x.strip() for x in " ".join(line).split("\t")]
    if line[0] not in conceptnet:
        conceptnet[line[0]] = []
    conceptnet[line[0]].append((line[1], line[2]))

quasimodo_raw_p = []
quasimodo_raw = []

with open(QUASIMODO_FILENAME) as f:
    for line in f:
        line_s = line.strip().split("\t")
        quasimodo_raw.append("\t".join([line_s[0], line_s[1], line_s[2], line_s[4]]))
        quasimodo_raw_p.append("\t".join([line_s[0], get_raw_predicate(line_s[1]), line_s[2], line_s[4]]))

quasimodo_raw_preprocessed = spacy_annotator.lemmatize_multiple(quasimodo_raw)

fact_common = []

for line, line_preprocessed in zip(quasimodo_raw, quasimodo_raw_preprocessed):
    s, p, o, n = [x.strip() for x in " ".join(line_preprocessed).split("\t")]
    if s not in conceptnet:
        continue
    elif (p, o) in conceptnet[s]:
        fact_common.append(line)
    else:
        po = p + " " + o
        for _, o in conceptnet[s]:
            if o == po:
                fact_common.append(line)
                break

with open("quasimodo/temp/conceptnet_annotations.tsv", "w") as f:
    for fact in fact_common:
        temp = [x.strip() for x in "".join(fact).split("\t")]
        f.write("\t".join(temp) + "\t" + "1\n")
