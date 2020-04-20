import json
res = []

with open("questions_examveda2.tsv") as f:
    res = []
    id = 0
    for line in f:
        line = line.strip().split("\t")
        if len(line) != 10:
            continue
        temp = dict()
        temp["id"] = str(id)
        id += 1
        temp["question"] = dict()
        temp["question"]["stem"] = line[0]
        temp["question"]["choices"] = []
        for i in [1, 3, 5, 7]:
            temp2 = dict()
            temp2["label"] = line[i]
            temp2["text"] = line[i+1]
            temp["question"]["choices"].append(temp2)
        temp["answerKey"] = line[-1]
        res.append(json.dumps(temp))

with open("questions_examveda.jsonl", "w") as f:
    f.write("\n".join(res))

# Our: 26.9%
# W2V: 25.6%
