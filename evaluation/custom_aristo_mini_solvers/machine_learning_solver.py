import json
import pickle
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import numpy as np

from aristomini.common.solver import SolverBase
from aristomini.common.models import MultipleChoiceQuestion, MultipleChoiceAnswer, ChoiceConfidence
from sklearn.linear_model import LogisticRegressionCV

from quasimodo.spacy_accessor import SpacyAccessor


class MachineLearningSolver(SolverBase):

    def __init__(self):
        super().__init__()
        self.name = "Machine Learning Solver"
        self.question_answer_label = []
        self.preprocessed_question_answer_label = []
        self.kb = None  # A pandas dataframe
        self.kb_grouped_s = None
        self.kb_grouped_p = None
        self.kb_grouped_o = None
        self.spacy_accessor = SpacyAccessor()
        self.clf = None

    def solver_info(self) -> str:
        return self.name

    def load_training_data_questions(self):
        questions = []
        with open("aristo-mini/questions/CommonsenseQAtrain_rand_split.jsonl") as f:
            for line in f:
                questions.append(json.loads(line.strip()))
        self.question_answer_label = []
        for question in questions:
            for choice in question["question"]["choices"]:
                self.question_answer_label.append((question["question"]["stem"],
                                                   choice["text"],
                                                   int(choice["label"] == question["answerKey"])))

    def preprocess_question_answer_label(self):
        questions = [" ".join(remove_stop_words(x[0].lower())) for x in self.question_answer_label]
        answers = [" ".join(remove_stop_words(x[1].lower())) for x in self.question_answer_label]
        questions_lemmatized = self.spacy_accessor.lemmatize_multiple(questions)
        answers_lemmatized = self.spacy_accessor.lemmatize_multiple(answers)
        self.preprocessed_question_answer_label = []
        for i in range(len(self.question_answer_label)):
            self.preprocessed_question_answer_label.append((questions_lemmatized[i],
                                                            answers_lemmatized[i],
                                                            self.question_answer_label[i][2]))
        return self.preprocessed_question_answer_label

    def group_kb(self):
        self.kb_grouped_s = self.kb.groupby(by="subject")
        self.kb_grouped_p = self.kb.groupby(by="predicate")
        self.kb_grouped_o = self.kb.groupby(by="object")

    def get_features_lemmatized(self, question, answer):
        p_and_o_with_s = 0
        p_with_s = 0
        o_with_s = 0
        double_link_s_to_o = 0

        if answer in self.kb_grouped_s.groups:
            for _, row in self.kb_grouped_s.get_group(answer).iterrows():
                if check_in(row["predicate"], question):
                    if check_in(row["object"], question):
                        p_and_o_with_s += row["score"]
                    else:
                        p_with_s += row["score"]
                elif check_in(row["object"], question):
                    o_with_s += row["score"]

        s_and_o_with_p = 0
        s_with_p = 0
        o_with_p = 0

        if answer in self.kb_grouped_p.groups:
            for _, row in self.kb_grouped_p.get_group(answer).iterrows():
                if check_in(row["subject"], question):
                    if check_in(row["object"], question):
                        s_and_o_with_p += row["score"]
                    else:
                        s_with_p += row["score"]
                elif check_in(row["object"], question):
                    o_with_p += row["score"]

        s_and_p_with_o = 0
        s_with_o = 0
        p_with_o = 0
        double_link_o_to_s = 0

        if answer in self.kb_grouped_o.groups:
            for _, row in self.kb_grouped_o.get_group(answer).iterrows():
                if check_in(row["subject"], question):
                    if check_in(row["predicate"], question):
                        s_and_p_with_o += row["score"]
                    else:
                        s_with_o += row["score"]
                elif check_in(row["predicate"], question):
                    p_with_o += row["score"]

        return np.array([p_and_o_with_s,
                         s_and_o_with_p,
                         s_and_p_with_o,
                         p_with_s,
                         o_with_s,
                         s_with_p,
                         o_with_p,
                         s_with_o,
                         p_with_o,
                         double_link_s_to_o,
                         double_link_o_to_s])

    def get_features_grouped_preprocessed(self, question, answer):
        question_lemmatized = " ".join(question)
        answer_lemmatized_split = answer
        result = None
        max_size = min(len(answer_lemmatized_split), 3)
        for size in range(max_size, 1, -1):
            for i in range(len(answer_lemmatized_split)):
                j = i + size
                to_add = self.get_features_lemmatized(question_lemmatized,
                                                      " ".join(answer_lemmatized_split[i:j])).astype(np.float64)
                to_add[np.isnan(to_add)] = 0.0
                if result is None:
                    result = to_add
                else:
                    result += to_add
            if result is not None:
                break
        if result is None:
            return [0.0] * 11
        return list(result)

    def get_features_from_preprocessed_qal(self, qal):
        return self.get_features_grouped_preprocessed(qal[0], qal[1])

    def get_all_features(self):
        all_features = []
        for i, qal in enumerate(self.preprocessed_question_answer_label):
            print(i, end="\r")
            all_features.append(self.get_features_from_preprocessed_qal(qal))
        return all_features

    def get_labels(self):
        y = []
        for qal in self.question_answer_label:
            y.append(qal[2])
        return y

    def train(self):
        self.load_training_data_questions()
        self.preprocess_question_answer_label()
        if self.kb_grouped_s is None:
            self.group_kb()
        X = np.array(self.get_all_features())
        y = np.array(self.get_labels())
        self.clf = LogisticRegressionCV(class_weight="balanced", cv=5)
        self.clf.fit(X, y)
        print("The score is %f" % (self.clf.score(X, y)))

    def save_model(self):
        with open("classifier_lr.pck", "wb") as f:
            pickle.dump(self.clf, f)

    def load_model(self):
        with open("classifier_rf.pck", "rb") as f:
            self.clf = pickle.load(f)

    def answer_question(self, question: MultipleChoiceQuestion) -> MultipleChoiceAnswer:
        # pylint: disable=unused-variable
        if self.clf is None:
            print("Load model")
            self.load_model()
        if self.kb_grouped_s is None:
            self.group_kb()

        print("Preprocessing question:")
        question_text = question.stem.lower()
        print(question_text)
        print("Preprocessing choices")
        choices = question.choices
        choice_texts = [x.text for x in choices]
        print(choice_texts)

        question_preprocessed = self.spacy_accessor.lemmatize(" ".join(remove_stop_words(question_text)))
        choices_preprocessed = [self.spacy_accessor.lemmatize(" ".join(remove_stop_words(choice.lower())))
                                for choice in choice_texts]

        print("Computing Confidence")
        confidences = self.predict_proba_positive(question_preprocessed, choices_preprocessed)
        print("Done.")

        return MultipleChoiceAnswer(
            [ChoiceConfidence(choice, confidence)
             for choice, confidence in zip(choices, confidences)]
        )

    def predict_proba_positive(self, question_text, choice_texts):
        features = [self.get_features_from_preprocessed_qal((question_text, choice)) for choice in choice_texts]
        X = np.array(features)
        y_prediction = self.clf.predict_proba(X)[:, 1]
        return y_prediction


stop_words = set(stopwords.words('english'))


def remove_stop_words(sentence):
    word_tokens = word_tokenize(sentence)
    return [w for w in word_tokens if w not in stop_words]


def check_in(word, sentence):
    regex = re.compile(r"(^|\s)" + re.escape(word) + r"($|\s)")
    return regex.search(sentence) is not None
