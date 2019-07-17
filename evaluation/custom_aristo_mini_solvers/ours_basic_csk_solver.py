from basic_csk_solver import BasicCSKSolver

class OurBasicCSKSolver(BasicCSKSolver):

    def __init__(self):
        self.name = "Ours Basic CSK solver"
        self.stoo = dict()
        self.otos = dict()
        with open("/home/julien/Documents/phd/CSK/quasimodo/temp/"
                  "quasimodo14.tsv") as f:
            for line in f:
                line = line.strip().split("\t")
                subj = self.lemmatize(line[0])
                pred = self.lemmatize(line[1])
                obj = self.lemmatize(line[2])
                score = float(line[5])
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
    solver = OurBasicCSKSolver()  # pylint: disable=invalid-name
    solver.run()
