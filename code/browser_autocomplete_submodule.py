from submodule_interface import SubmoduleInterface
import time
import corenlp
from generated_fact import GeneratedFact
from inputs import Inputs
from string import ascii_lowercase
import inflect

max_query_length = 100000

class BrowserAutocompleteSubmodule(SubmoduleInterface):
    """BrowserAutocompleteSubmodule
    Represents the autocomplete from a web search engine
    """

    def __init__(self, module_reference):
        self.time_between_queries = 1.0 # The time between two queries
        self.default_number_suggestions = 8 # The maximum number of suggestions

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

    def process(self, input_interface):
        # Needs subjects
        if not input_interface.has_subjects():
            return input_interface

        suggestions = []

        for pattern in input_interface.get_patterns("google-autocomplete"):
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
                                            (x[0], x[1], pattern),
                                            base_suggestions))
                # add to the list of suggestions
                suggestions += list(filter(lambda x: pattern.match(x[0]),
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
                        temp = list(map(lambda x:
                                        (x[0], x[1], pattern), temp))
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

        # OPENIE part
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
                        #"openie.triple.strict" : "true",
                        "openie.max_entailments_per_clause":"1000"})
        generated_facts = []
        subjects = set()

        # I still have to transform into a plural for subject checking
        plural_engine = inflect.engine()
        for subject in input_interface.get_subjects():
            subjects.add(subject.get())
            subjects.add(plural_engine.plural(subject.get()))

        full_sentence = []

        for suggestion in suggestions:
            # question to statement
            # TODO Improve it
            # We need this because of OpenIE very bad with questions
            original = suggestion[0]
            l = suggestion[0].split(" ")
            new_sentence = ""
            if "do" in l[1]:
                new_sentence = " ".join(l[2:])
            elif "are" in l[1]:
                if " ".join(l[2:4]) in subjects:
                    new_sentence = " ".join(l[2:4] + \
                                             ["are"] + l[4:])
                elif l[2] in subjects:
                    new_sentence = " ".join([l[2]] + \
                                             ["are"] + l[3:])
            full_sentence.append(new_sentence)

        full_sentence = list(filter(lambda x: len(x) > 0, full_sentence))

        batches = []

        begin = 0
        counter = 0
        for i in range(len(full_sentence)):
            if counter + 2 + len(full_sentence[i]) > max_query_length:
                batches.append(". ".join(full_sentence[begin:i]) + ".")
                begin = i
                counter = 0
            counter += len(full_sentence[i]) + 2
        batches.append(". ".join(full_sentence[begin:]) + ".")

        for batch in batches:
            # We annotate the sentence
            # And extract the triples
            print("before")
            out = nlp.annotate(batch)
            print("after")
            for sentence in out.sentence:
                for triple in sentence.openieTriple:
                    subject = triple.subject
                    if subject not in subjects:
                        continue
                    obj = triple.object
                    predicate = triple.relation
                    score = triple.confidence
                    generated_facts.append(
                        GeneratedFact(
                            subject,
                            predicate,
                            obj,
                            None,
                            False,
                            # For the score, inverse the ranking (higher is
                            # better) and add the confidence of the triple
                            self.default_number_suggestions - suggestion[1] +
                                score,
                            original,
                            self._module_reference,
                            self,
                            suggestion[2]))
        # stop the annotator
        nlp.stop()

        return input_interface.add_generated_facts(generated_facts)