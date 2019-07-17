from basic_csk_solver import BasicCSKSolver

class WebChildBasicCSKSolver(BasicCSKSolver):

    def __init__(self):
        self.name = "Webchild Basic CSK solver"
        self.subject_to_objects = dict()
        self.object_to_subjects = dict()
        with open("/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/"
                  "commonsense_data/Webchild/webchild_20k.tsv") as f:
            for line in f:
                line = line.strip().split("\t")
                subj = line[0]
                pred = line[1]
                obj = line[2]
                score = 1.0
                if subj in self.subject_to_objects:
                    self.subject_to_objects[subj].append((obj, score))
                    self.subject_to_objects[subj].append((pred, score))
                else:
                    self.subject_to_objects[subj] = [(obj, score), (pred, score)]
                if obj in self.object_to_subjects:
                    self.object_to_subjects[obj].append((subj, score))
                    self.object_to_subjects[obj].append((pred, score))
                else:
                    self.object_to_subjects[obj] = [(subj, score), (pred, score)]
                if pred in self.object_to_subjects:
                    self.object_to_subjects[pred].append((subj, score))
                    self.object_to_subjects[pred].append((obj, score))
                else:
                    self.object_to_subjects[pred] = [(subj, score), (obj, score)]
        for subj in self.subject_to_objects:
            d_temp = dict()
            for value in self.subject_to_objects[subj]:
                obj = value[0]
                score = value[1]
                if obj in d_temp:
                    d_temp[obj].append(score)
                else:
                    d_temp[obj] = [score]
            self.subject_to_objects[subj] = []
            for obj in d_temp:
                self.subject_to_objects[subj].append((obj, max(d_temp[obj])))
        for subj in self.object_to_subjects:
            d_temp = dict()
            for value in self.object_to_subjects[subj]:
                obj = value[0]
                score = value[1]
                if obj in d_temp:
                    d_temp[obj].append(score)
                else:
                    d_temp[obj] = [score]
            self.object_to_subjects[subj] = []
            for obj in d_temp:
                self.object_to_subjects[subj].append((obj, max(d_temp[obj])))


if __name__ == "__main__":
    solver = WebChildBasicCSKSolver()  # pylint: disable=invalid-name
    solver.run()
