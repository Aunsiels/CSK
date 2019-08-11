from basic_csk_solver import BasicCSKSolver


class OurBasicCSKSolver(BasicCSKSolver):

    def __init__(self):
        super().__init__()
        self.name = "Ours Basic CSK solver"
        self.subject_to_objects = dict()
        self.object_to_subjects = dict()
        with open("/home/julien/Documents/phd/CSK/quasimodo/temp/"
                  "quasimodo17.tsv") as f:
            raw_triples = f.readlines()
        raw_lemmatized_triples = self.spacy_accessor.lemmatize_multiple(raw_triples)
        for line in raw_lemmatized_triples:
            line = " ".join(line)
            line = line.strip().split("\t")
            subj = line[0].strip()
            pred = line[1].strip()
            obj = line[2].strip()
            score = float(line[5])
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
    solver = OurBasicCSKSolver()  # pylint: disable=invalid-name
    solver.run()
