from quasimodo.serializable import Serializable


class MultipleScore(Serializable):

    def to_dict(self):
        res = dict()
        res["type"] = "MultipleScore"
        res["scores"] = []
        for score in self.scores:
            res["scores"].append(
                {"score": score[0],
                "module_from": score[1].to_dict(),
                "submodule_from": score[2].to_dict()}
            )
        return res

    def __init__(self):
        self.scores = []

    def add_score(self, score, module_from, submodule_from):
        self.scores.append((score, module_from, submodule_from))

    def __add__(self, other):
        new_scores = MultipleScore()
        for score in self.scores + other.scores:
            new_scores.add_score(score[0], score[1], score[2])
        return new_scores

    def add(self, other):
        for score in other.scores:
            self.add_score(score[0], score[1], score[2])

    def __str__(self):
        return "MultipleScore(" + " // ".join([", ".join(map(str, x)) for x in self.scores]) + ")"