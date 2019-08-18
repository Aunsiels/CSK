import pandas as pd

from machine_learning_solver import MachineLearningSolver


class MachineLearningQuasimodoSolver(MachineLearningSolver):

    def __init__(self):
        super().__init__()
        self.name = "Quasimodo ML solver"
        self.load_kb()

    def load_kb(self):
        kb_raw = []
        raw_triples = []
        print("Loading KB...")
        with open("/home/julien/Documents/phd/CSK/quasimodo/temp/quasimodo17.tsv") as f:
            for line in f:
                line = line.strip().split("\t")
                kb_raw.append(line[:-1])
                raw_triples.append("\t".join(line[0:3]))
        print("Lemmatizing KB")
        raw_lemmatized_triples = self.spacy_accessor.lemmatize_multiple(raw_triples)
        kb = []
        for line in raw_lemmatized_triples:
            line = " ".join(line)
            line = line.strip().split("\t")
            subj = line[0].strip()
            pred = line[1].strip()
            if len(line) > 2:
                obj = line[2].strip()
            else:
                obj = ""
            kb.append([subj, pred, obj])
        print("Final cleaning")
        self.kb = pd.DataFrame(kb_raw,
                               columns=["subject", "predicate", "object", "modality", "is_negative", "score"])
        df_spo_lemma = pd.DataFrame(kb, columns=["subject", "predicate", "object"])
        self.kb["subject"] = df_spo_lemma["subject"]
        self.kb["predicate"] = df_spo_lemma["predicate"]
        self.kb["object"] = df_spo_lemma["object"]
        self.kb["score"] = pd.to_numeric(self.kb["score"])
        self.kb["predicate"] = [transform_predicate(x) for x in self.kb["predicate"]]


def transform_predicate(predicate):
    if predicate == "has_body_part":
        return "have"
    if "has_" in predicate:
        return "be"
    return predicate


if __name__ == "__main__":
    solver = MachineLearningQuasimodoSolver()  # pylint: disable=invalid-name
    solver.run()
