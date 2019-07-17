from basic_csk_solver import BasicCSKSolver

class TupleKBBasicCSKSolver(BasicCSKSolver):

    def __init__(self):
        self.name = "TupleKB Basic CSK solver"
        self.stoo = dict()
        self.otos = dict()
        with open("/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/"
                  "commonsense_data/TupleKB/aristo-tuple-kb-v5-mar2017/"
                  "tuplekb_20k.tsv") as f:
            for line in f:
                line = line.strip().split("\t")
                subj = line[0]
                pred = line[1]
                obj = line[2]
                score = 1.0
                if subj in self.stoo:
                    self.stoo[subj].append((obj, score))
                    self.stoo[subj].append((pred, score))
                else:
                    self.stoo[subj] = [(obj, score), (pred, score)]
                if obj in self.otos:
                    self.otos[obj].append((subj, score))
                    self.otos[obj].append((pred, score))
                else:
                    self.otos[obj] = [(subj, score), (pred, score)]
                if pred in self.otos:
                    self.otos[pred].append((subj, score))
                    self.otos[pred].append((obj, score))
                else:
                    self.otos[pred] = [(subj, score), (obj, score)]
        for subj in self.stoo:
            d_temp = dict()
            for value in self.stoo[subj]:
                obj = value[0]
                score = value[1]
                if obj in d_temp:
                    d_temp[obj].append(score)
                else:
                    d_temp[obj] = [score]
            self.stoo[subj] = []
            for obj in d_temp:
                self.stoo[subj].append((obj, max(d_temp[obj])))
        for subj in self.otos:
            d_temp = dict()
            for value in self.otos[subj]:
                obj = value[0]
                score = value[1]
                if obj in d_temp:
                    d_temp[obj].append(score)
                else:
                    d_temp[obj] = [score]
            self.otos[subj] = []
            for obj in d_temp:
                self.otos[subj].append((obj, max(d_temp[obj])))


if __name__ == "__main__":
    solver = TupleKBBasicCSKSolver()  # pylint: disable=invalid-name
    solver.run()
