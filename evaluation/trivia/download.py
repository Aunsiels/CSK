import json
import urllib.request
from random import shuffle

# All
all_cat = "https://opentdb.com/api.php?amount=50&type=multiple"
# Animals
animals_cat = "https://opentdb.com/api.php?amount=38&category=27&type=multiple"

res = []

id = 0
questions = set()
for _ in range(10):
    contents = json.loads(urllib.request.urlopen(all_cat).read())
    labels = ["A", "B", "C", "D", "E", "F", "G"]
    for result in contents["results"]:
        if result["question"] in questions:
            continue
        temp = dict()
        temp["id"] = str(id)
        id += 1
        temp["question"] = dict()
        temp["question"]["stem"] = result["question"]
        questions.add(result["question"])
        temp["question"]["choices"] = []
        answer = result["correct_answer"]
        choices = [result["correct_answer"]] + result["incorrect_answers"]
        shuffle(choices)
        for i in range(len(choices)):
            temp2 = dict()
            temp2["label"] = labels[i]
            temp2["text"] = choices[i]
            temp["question"]["choices"].append(temp2)
            if choices[i] == answer:
                temp["answerKey"] = labels[i]
        res.append(json.dumps(temp))

with open("questions_trivia_allcat.jsonl", "w", encoding="utf-8") as f:
    f.write("\n".join(res))
