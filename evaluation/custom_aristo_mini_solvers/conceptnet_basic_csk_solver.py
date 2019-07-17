from basic_csk_solver import BasicCSKSolver

class ConceptNetBasicCSKSolver(BasicCSKSolver):

    def __init__(self):
        self.name = "ConceptNet Basic CSK solver"
        self.subject_to_objects = dict()
        self.object_to_subjects = dict()
        with open("/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/"
                  "commonsense_data/ConceptNet/conceptnet_20k.tsv") as f:
            for line in f:
                line = line.strip().split("\t")
                subj = line[0]
                obj = line[2]
                score = 1.0
                if subj in self.subject_to_objects:
                    self.subject_to_objects[subj].append((obj, score))
                else:
                    self.subject_to_objects[subj] = [(obj, score)]
                if obj in self.object_to_subjects:
                    self.object_to_subjects[obj].append((subj, score))
                else:
                    self.object_to_subjects[obj] = [(subj, score)]
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
    solver = ConceptNetBasicCSKSolver()  # pylint: disable=invalid-name
    solver.run()
