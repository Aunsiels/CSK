from submodule_interface import SubmoduleInterface
import time
import corenlp
from generated_fact import GeneratedFact
from inputs import Inputs
from string import ascii_lowercase
import inflect
import logging
import spacy
import os

max_query_length = 100000
nlp = spacy.load('en_core_web_sm')
cache_dir = "question2statement/"
filename = "cache.tsv"
plural_engine = inflect.engine()

class BrowserAutocompleteSubmodule(SubmoduleInterface):
    """BrowserAutocompleteSubmodule
    Represents the autocomplete from a web search engine
    """

    def __init__(self, module_reference):
        self.time_between_queries = 1.0 # The time between two queries
        self.default_number_suggestions = 8 # The maximum number of suggestions
        self._module_reference = module_reference
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        # Load previous q2s
        self._q2s = dict()
        self._load_q2s()

    def _load_q2s(self):
        if os.path.isfile(cache_dir + filename):
            with open(cache_dir + filename) as f:
                for line in f:
                    line = line.strip().split("\t")
                    if len(line) < 2:
                        continue
                    self._q2s[line[0]] = line[1]

    def _save_q2s(self, question, statement, subject):
        with open(cache_dir + filename, "a") as f:
            f.write(question.strip() + "\t" + statement.strip() +
                    "\t" + subject + "\n")

    def get_suggestion(self, query, lang="en", ds=""):
        """get_suggestion
        Gets suggestion from the browser to a give query
        :param query: the query to autocomplete
        :type query: str
        :param lang: the language to use
        :type lang: str
        :param ds: An additional parameter
        :type ds: str
        :return: A list of scored autosuggestions with a whether the cache was
        used or not
        :rtype: List[((str, float), bool)]
        """
        raise NotImplementedError

    def _get_all_suggestions(self, input_interface):
        suggestions = []

        for pattern in input_interface.get_patterns("google-autocomplete"):
            logging.info("Processing " + pattern.to_str())
            for subject in input_interface.get_subjects():
                temp = ""
                # Generate the query
                base_query = pattern.to_str_subject(subject)
                base_suggestions, cache = self.get_suggestion(base_query)
                # Exceeded number of requests
                if base_suggestions is None:
                    break
                # Append the patterns
                base_suggestions = list(map(lambda x:
                                            (x[0], x[1], pattern,
                                             subject.get()),
                                            base_suggestions))
                # add to the list of suggestions
                suggestions += list(filter(lambda x: pattern.match(x[0]),
                                           base_suggestions))
                base_sentences = list(map(lambda x: x[0],
                                          base_suggestions))
                if not cache:
                    time.sleep(self.time_between_queries)
                # There might be more suggestions
                if len(base_suggestions) == self.default_number_suggestions:
                    # Artificially add more suggestions
                    # TODO: To this recursively
                    for c in ascii_lowercase:
                        temp, cache = self.get_suggestion(base_query + " " + c)
                        if temp is None:
                            break
                        # Check not seen before
                        temp = list(filter(lambda x: x[0] not in base_sentences,
                                           temp))
                        temp = list(map(lambda x:
                                        (x[0],
                                         x[1] + self.default_number_suggestions,
                                         pattern,
                                         subject.get()), temp))
                        suggestions += list(filter(lambda x:
                                                       pattern.match(x[0]),
                                                   temp))
                        # We sleep only if the data was not cached
                        if not cache:
                            time.sleep(self.time_between_queries)
                    if temp is None:
                        break
            if temp is None or base_suggestions is None:
                break
        return suggestions

    def _to_statement(self, question, subject):
        subject2 = plural_engine.plural(subject)
        if question.strip() in self._q2s:
            return self._q2s[question.strip()]
        tokens = []
        pos = []
        statement = ""
        for token in nlp(question):
            if token.text == "'s":
                tokens[-1] = tokens[-1] + "'s"
                pos[-1] = (pos[-1][0] + "'s", pos[-1][1])
            elif token.text == "?":
                continue
            else:
                tokens.append(token.text)
                pos.append((token.text, token.tag_))
        begin = []
        middle = []
        end = []
        if tokens[1] == "are" or tokens[1] == "is":
            found_noun = False
            found_second = False
            found_something_else = False
            found_final_adj = False
            found_cc = False
            found_in = False
            for p in pos[2:]:
                if not found_noun and \
                        ((subject in " ".join(begin) + " " + p[0] or \
                         subject2 in " ".join(begin) + " " + p[0]) \
                         and (not found_cc or "NN" in p[1] or "VBZ" in p[1])):
                    found_noun = True
                    begin.append(p[0])
                elif found_noun and not found_something_else and \
                        not found_second and ("CC" in p[1] or "of" == p[0]):
                    found_cc = True
                    found_noun = False
                    begin.append(p[0])
                elif found_noun and not found_something_else and found_second\
                        and ("CC" in p[1] or "of" == p[0]):
                    found_second = False
                    end.append(p[0])
                elif not found_something_else and found_noun and \
                        ("NN" in p[1] or "IN" in p[0])\
                        and not found_final_adj:
                    if "IN" in p[0]:
                        found_in = True
                    found_second = True
                    end.append(p[0])
                elif not found_noun:
                    begin.append(p[0])
                else:
                    if "JJ" in p[1]:
                        found_final_adj = True
                    found_something_else = True
                    middle.append(p[0])
            if len(begin) == 0:
                statement = ""
            elif len(middle) == 0 and len(end) == 0:
                statement = ""
            elif len(middle) == 0:
                statement = " ".join(begin) + " " + tokens[1] + \
                    " " + " ".join(end)
            elif len(end) == 0:
                statement =  " ".join(begin) + " " + tokens[1] + " " +\
                    " ".join(middle)
            elif found_in:
                statement = " ".join(begin) + " " + tokens[1] + " " + \
                    " ".join(middle) + \
                    " " + \
                    " ".join(end)
            else:
                statement = " ".join(begin) + " have " + " ".join(middle) + \
                    " " +\
                    " ".join(end)
        elif tokens[1] == "do" or tokens[1] == "does":
            statement = " ".join(tokens[2:])
        elif tokens[1] == "can" or tokens[1] == "could" or \
                tokens[1] == "cannot":
            # Look for first verb, in base form
            for i in range(len(pos)):
                p = pos[i]
                if p[1] == "VBP" or p[1] == "VB":
                    statement = " ".join(tokens[2:i]) + " " + tokens[1] + " " +\
                        " ".join(tokens[i:])
                    break
        elif tokens[1] == "ca" and tokens[2] == "n't":
            # I have to turn it to an affirmation to make openIE work
            temp = self._to_statement(tokens[0] + " can " +
                                      " ".join(tokens[3:]), subject)
            statement = temp
            # return temp.replace(" can ", " cannot ")
        else:
            statement = question
        self._save_q2s(question, statement, subject)
        return statement
    def _compute_batch_openie(self, suggestions, input_interface):
        subjects = set()

        # I still have to transform into a plural for subject checking
        for subject in input_interface.get_subjects():
            subjects.add(subject.get())
            subjects.add(plural_engine.plural(subject.get()))

        full_sentence = []

        logging.info("Transformation questions to statement")
        for suggestion in suggestions:
            # question to statement
            # We need this because of OpenIE very bad with questions
            new_sentence = self._to_statement(suggestion[0], suggestion[3])
            if new_sentence[:6] == "there ":
                new_sentence = new_sentence[6:]
            if " are not " in new_sentence:
                full_sentence.append((new_sentence.replace(" are not ",
                                                           " are "),
                                      suggestion[1],
                                      suggestion[2],
                                      True))
            if new_sentence != "":
                full_sentence.append((new_sentence,
                                      suggestion[1],
                                      suggestion[2],
                                      False))

        full_sentence = list(filter(lambda x: len(x[0]) > 0, full_sentence))

        batches = []

        begin = 0
        counter = 0
        for i in range(len(full_sentence)):
            if counter + 3 + len(full_sentence[i][0]) > max_query_length:
                batches.append(full_sentence[begin:i])
                begin = i
                counter = 0
            counter += len(full_sentence[i][0]) + 3
        batches.append(full_sentence[begin:])
        return batches

    def _simple_extraction(self, sentence):
        tokens = []
        for token in nlp(sentence):
            tokens.append(token.text)
        if len(tokens) == 3 and tokens[1].lower() in ["can", "cannot"]:
            return tokens
        return None

    def _get_generated_facts(self, batches):
        # Open a server
        # TODO: is there a problem if several in parallel ?
        # Should play with start_server?
        nlp = corenlp.CoreNLPClient(
            start_server=True,
            endpoint='http://localhost:9000',
            timeout=1000000,
            annotators=['openie'],
            properties={'annotators': 'openie',
                        'inputFormat': 'text',
                        'outputFormat': 'json',
                        'serializer': 'edu.stanford.nlp.pipeline.ProtobufAnnotationSerializer',
                        'openie.affinity_probability_cap': '1.0',
                        #"openie.triple.strict" : "true",
                        "openie.max_entailments_per_clause":"500"})

        generated_facts = []

        for batch in batches:
            # We annotate the sentence
            # And extract the triples
            sentences = " . ".join([x[0].replace(".", "").replace("?", "")
                                    for x in batch])\
                + " . "
            out = nlp.annotate(sentences)
            counter = 0
            for sentence in out.sentence:
                suggestion = batch[counter]
                sugg_temp = " ".join(
                    filter(lambda x: x != ".",
                           [x.word for x in sentence.token]))
                sugg_temp = sugg_temp.replace("-LRB-", "(")
                sugg_temp = sugg_temp.replace("-RRB-", ")")
                if sugg_temp.replace(" ", "").replace("'", "")\
                        .replace("`", "").replace(".", "").replace("?", "")\
                        != suggestion[0].replace(" ", "").replace("'", "")\
                        .replace("`", "").replace(".", "").replace("?", ""):
                    logging.error("The subjects do not match. Received: %s,"
                                  "Expecting: %s", sugg_temp, suggestion)
                    break
                maxi_length_predicate = 1
                for triple in sentence.openieTriple:
                    predicate = triple.relation
                    maxi_length_predicate = max(len(predicate.split(" ")),
                                                maxi_length_predicate)
                if len(sentence.openieTriple) == 0:
                    # Try simple extraction as OpenIE is bad for this
                    se = self._simple_extraction(suggestion[0])
                    if se is not None:
                        score = 1.0
                        negative = False
                        if suggestion[2] is not None:
                            negative = suggestion[2].is_negative()
                        if suggestion[3]:
                            negative = True
                        generated_facts.append(
                            GeneratedFact(
                                se[0],
                                se[1],
                                se[2],
                                None,
                                negative,
                                # For the score, inverse the ranking (higher is
                                # better) and add the confidence of the triple
                                (2 * self.default_number_suggestions - suggestion[1]
                                    ) /
                                    (2 * self.default_number_suggestions) *
                                    score,
                                suggestion[0],
                                self._module_reference,
                                self,
                                suggestion[2]))
                for triple in sentence.openieTriple:
                    subject = triple.subject
                    obj = triple.object
                    predicate = triple.relation
                    score = triple.confidence
                    # prefer longer predicate ?
                    score *= len(predicate.split(" ")) / maxi_length_predicate
                    negative = False
                    if suggestion[2] is not None:
                        negative = suggestion[2].is_negative()
                    generated_facts.append(
                        GeneratedFact(
                            subject,
                            predicate,
                            obj,
                            None,
                            negative,
                            # For the score, inverse the ranking (higher is
                            # better) and add the confidence of the triple
                            (2 * self.default_number_suggestions - suggestion[1]
                                ) /
                                (2 * self.default_number_suggestions) *
                                score,
                            suggestion[0],
                            self._module_reference,
                            self,
                            suggestion[2]))
                counter += 1
        # stop the annotator
        nlp.stop()
        return generated_facts

    def process(self, input_interface):
        # Needs subjects
        logging.info("Start submodule %s", self.get_name())
        if not input_interface.has_subjects():
            return input_interface

        suggestions = self._get_all_suggestions(input_interface)


        # OPENIE part
        batches = self._compute_batch_openie(suggestions, input_interface)
        generated_facts = self._get_generated_facts(batches)


        return input_interface.add_generated_facts(generated_facts)
