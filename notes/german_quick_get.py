from quasimodo.google_autocomplete_submodule import GoogleAutocompleteSubmodule, look_new

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t" , "u", "v", "w", "x", "y", "z"]

question_words = ["Warum", "Wieso", "Weshalb"]
verbs = ["sind", "sind die", "haben", "haben die", "können",
        "können die", "brauchen", "brauchen die", "wollen", "werden", "hatten", "wissen",
        "glauben", "denken"]
nationalities = ["Amerikaner", "Briten", "Franzosen", "Spanier",
        "Italiener", "Holländer", "Polen", "Russen", "Türken",
        "Inder", "Chinesen", "Japaner", "Koreaner", "Brasilianer",
        "Schweden", "Österreicher", "Schweizer", "Niederländer", "Finnen",
        "Dänen", "Iren", "Rumänen", "Kanadier", "Afrikaner", "Araber", "Asiaten", "Deutsche",
                 "Katholiken", "Juden", "Muslime", "Buddhisten",
                  "Schwarze", "Weiße"]

google_autocomplete = GoogleAutocompleteSubmodule(None, cache_name="google-cache-german")
look_new = True
result = []

total = len(question_words) * len(verbs) * len(nationalities)
counter = 0

for question_word in question_words:
    for verb in verbs:
        for nationality in nationalities:
            print(counter / total * 100, "% done")
            base = question_word + " " + verb + " " + nationality
            temp = google_autocomplete.get_suggestion(base,
                    lang="de")[0]
            temp = [nationality + "\t" + x[0] for x in temp]
            print(temp)
            if temp:
                result.append("\n".join(temp))
                for letter in alphabet:
                    temp = google_autocomplete.get_suggestion(base + " " + letter,
                            lang="de")[0]
                    temp = [nationality + "\t" + x[0] for x in temp]
                    print(temp)
                    if temp:
                        result.append("\n".join(temp))
            counter += 1

with open("result_german.txt", "w") as f:
    f.write("\n".join(result))
