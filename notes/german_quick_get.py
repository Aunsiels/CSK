from quasimodo.google_autocomplete_submodule import GoogleAutocompleteSubmodule

question_words = ["Warum", "Wieso", "Weshalb"]
verbs = ["sind", "sind die", "haben", "haben die", "können",
        "können die", "brauchen", "brauchen die", "wollen", "werden", "hatten", "wissen",
        "glauben", "denken"]
nationalities = ["Amerikaner", "Briten", "Franzosen", "Spanier",
        "Italiener", "Holländer", "Polen", "Russen", "Türken",
        "Inder", "Chinesen", "Japaner", "Koreaner", "Brasilianer",
        "Schweden", "Österreicher", "Schweizer", "Niederländer", "Finnen",
        "Dänen", "Iren", "Rumänen", "Kanadier", "Afrikaner", "Araber", "Asiaten", "Deutsche"] 

google_autocomplete = GoogleAutocompleteSubmodule(None, cache_name="google-cache-german")
result = []

total = len(question_words) * len(verbs) * len(nationalities)
counter = 0

for question_word in question_words:
    for verb in verbs:
        for nationality in nationalities:
            print(counter / total * 100, "% done")
            result.append("\n".join(google_autocomplete.get_suggestion(question_word + " " + verb + " " + nationality,
                    lang="de")[0]))
            counter += 1

with open("result_german.txt", "w") as f:
    f.write("\n".join(result))
