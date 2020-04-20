import urllib.request
from bs4 import BeautifulSoup
import re

for section in range(1, 3):
    for page in range(1, 1000):
        questions_text = []
        contents = urllib.request.urlopen("https://www.examveda.com/general-knowledge/"
            "practice-mcq-question-on-general-science/?section=" +
            # "practice-mcq-question-on-basic-general-knowledge/?section=" +
            str(section) + "&page=" + str(page)).read()
        soup = BeautifulSoup(contents)
        questions = soup.findAll("article",
            {"class": "question single-question question-type-normal"})
        if len(questions) == 0:
            break
        for question_article in questions:
            question = question_article.findAll("div",
                {"class": "question-main"})
            if len(question) != 1:
                continue
            else:
                question = question[0].getText()
            propositions = question_article.findAll("div",
                {"class": "form-inputs clearfix question-options"})
            if len(propositions) != 1:
                continue
            else:
                propositions = [x.getText().strip().strip(".")
                                for x in propositions[0].findAll("label")]
            answer = question_article.findAll("div",
                {"class": "row answer_container"})
            if len(answer) != 1:
                continue
            else:
                answer = [x.getText().replace("Option ", "").strip()
                          for x in answer[0].findAll("strong")]
            if len(answer) != 1:
                continue
            else:
                answer = answer[0]
            questions_text.append(question +
                "\t" + "\t".join(propositions) +
                "\t" + answer)
        if len(questions_text) == 0:
            break
        else:
            with open("questions_examveda_science.tsv", "a") as f:
                f.write("\n".join(questions_text) + "\n")
