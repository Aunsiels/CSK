import re
import inflect
import logging
import corenlp
import spacy
from generated_fact import GeneratedFact
from statement_maker import StatementMaker
from inputs import Inputs
from submodule_interface import SubmoduleInterface
from modality import Modality

_nlp = spacy.load('en_core_web_sm')
_plural_engine = inflect.engine()

class OpenIEFactGeneratorSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self.statement_maker = StatementMaker()
        self._max_query_length = 99990
        self.default_number_suggestions = 8 # The maximum number of suggestions
        self._module_reference = module_reference

    def _compute_batch_openie(self, suggestions, input_interface):
        subjects = set()

        # I still have to transform into a plural for subject checking
        for subject in input_interface.get_subjects():
            subjects.add(subject.get())
            subjects.add(_plural_engine.plural(subject.get()))

        full_sentence = []

        logging.info("Transformation questions to statement")
        for suggestion in suggestions:
            # question to statement
            # We need this because of OpenIE very bad with questions
            new_sentence = self.statement_maker.to_statement(suggestion[0],
                                                             suggestion[3])
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
            if counter + 3 + len(full_sentence[i][0]) > self._max_query_length:
                batches.append(full_sentence[begin:i])
                begin = i
                counter = 0
            counter += len(full_sentence[i][0]) + 3
        batches.append(full_sentence[begin:])
        return batches

    def _simple_extraction(self, sentence):
        tokens = []
        for token in _nlp(sentence):
            tokens.append(token.text)
        if len(tokens) == 3 and tokens[1].lower() in ["can", "cannot"]:
            return tokens
        elif len(tokens) == 2:
            return [tokens[0], "can", tokens[1]]
        return None

    def _try_extend(self, subj, pred, obj, sentence):
        # works for short sentences
        # But some problems with adjectives
        # eg african people have big nose and lips
        end = obj + " and "
        pos = sentence.find(end)
        if pos != -1:
            new_obj = sentence[pos + len(end):].strip()
            if " " not in new_obj:
                return (subj, pred, new_obj)
        return None

    def get_generated_facts(self, suggestions, input_interface):
        batches = self._compute_batch_openie(suggestions, input_interface)
        regex = re.compile("[^a-zA-Z]")
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
            sentences = " . ".join([x[0].replace(".", "").replace("?", "").replace("!", "")
                                    for x in batch])\
                + " . "
            try:
                out = nlp.annotate(sentences)
            except corenlp.client.AnnotationException:
                logging.info("Annotation Error with: " + sentences)
            counter = 0
            for sentence in out.sentence:
                if counter >= len(batch):
                    logging.error("The counter and the batch do not match."
                                  " Expected: %d, Received: %d",
                                  len(batch), counter)
                    break
                suggestion = batch[counter]
                if len(sentence.token) == 0:
                    counter += 1
                    logging.debug("Empty sentence encountered")
                    continue
                sugg_temp = " ".join(
                    filter(lambda x: x != ".",
                           [x.word for x in sentence.token]))
                sugg_temp = sugg_temp.replace("-LRB-", "(")
                sugg_temp = sugg_temp.replace("-RRB-", ")")
                sugg_temp = sugg_temp.replace("-LSB-", "[")
                sugg_temp = sugg_temp.replace("-RSB-", "]")
                sugg_temp = sugg_temp.replace("-LCB-", "{")
                sugg_temp = sugg_temp.replace("-RCB-", "}")
                sugg_temp = sugg_temp.replace("&amp;", "&")
                if regex.sub("", sugg_temp) != regex.sub("", suggestion[0]):
                    logging.error("The subjects do not match. Received: %s,"
                                  "Expecting: %s", sugg_temp, suggestion)
                    # Check if we went too fast
                    suggestion = batch[counter - 1]
                    if regex.sub("", sugg_temp) != regex.sub("", suggestion[0]):
                        counter += 1
                        continue
                    else:
                        counter -= 1
                maxi_length_predicate = 1
                maxi_length_object = 1
                maxi_obj = ""
                contains_than = False
                for triple in sentence.openieTriple:
                    predicate = triple.relation
                    maxi_length_predicate = max(predicate.count(" ") + 1,
                                                maxi_length_predicate)
                for triple in sentence.openieTriple:
                    predicate = triple.relation
                    obj = triple.object
                    if " than " in obj:
                        contains_than = True
                    if maxi_length_predicate == predicate.count(" ") + 1:
                        if obj.count(" ") + 1 > maxi_length_object:
                            maxi_length_object = obj.count(" ") + 1
                            maxi_obj = obj
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
                additional_triples = []
                for triple in sentence.openieTriple:
                    subject = triple.subject
                    obj = triple.object
                    predicate = triple.relation
                    # This is to prevent too many extractions
                    # If it useful in practice to extract more than one fact?
                    if maxi_length_predicate != predicate.count(" ") + 1:
                        continue
                    score = triple.confidence
                    # prefer longer predicate ?
                    score *= (predicate.count(" ") + 1) / maxi_length_predicate
                    # prefer longer extractions
                    # 2 spaces at least
                    score_extr = (len(subject) + len(obj) + len(predicate) + 2)\
                        / len(suggestion[0])
                    negative = False
                    if suggestion[2] is not None:
                        negative = suggestion[2].is_negative()
                    modality = None
                    modality_temp = ""
                    # For comparisons only full objects
                    if maxi_length_object != obj.count(" ") + 1 and contains_than:
                        continue
                    if maxi_length_object != obj.count(" ") + 1:
                        modality_temp = "TBC[" + maxi_obj + "]"
                    if suggestion[0].find(subject) != 0 and \
                            suggestion[0].find("a " + subject) != 0 and\
                            suggestion[0].find("the " + subject) != 0:
                        if modality_temp:
                            modality_temp += " "
                        modality = Modality(modality_temp + "some[subj]")
                    else:
                        modality = Modality(modality_temp)
                    generated_facts.append(
                        GeneratedFact(
                            subject,
                            predicate,
                            obj,
                            modality,
                            negative,
                            # For the score, inverse the ranking (higher is
                            # better) and add the confidence of the triple
                            (2 * self.default_number_suggestions - suggestion[1]
                                ) /
                                (2 * self.default_number_suggestions) *
                                score * score_extr,
                            suggestion[0],
                            self._module_reference,
                            self,
                            suggestion[2]))
                    spo = self._try_extend(subject,
                                           predicate,
                                           obj,
                                           suggestion[0])
                    if spo is not None:
                        score_extr = (len(spo[0]) + len(spo[1]) + len(spo[2])
                                          + 2)\
                            / len(suggestion[0])
                        modality = None
                        if suggestion[0].find(spo[0]) != 0:
                            modality = Modality("some[subj]")
                        generated_facts.append(
                            GeneratedFact(
                                spo[0],
                                spo[1],
                                spo[2],
                                modality,
                                negative,
                                # For the score, inverse the ranking (higher is
                                # better) and add the confidence of the triple
                                (2 * self.default_number_suggestions -
                                        suggestion[1]) /
                                    (2 * self.default_number_suggestions) *
                                    score * score_extr,
                                suggestion[0],
                                self._module_reference,
                                self,
                                suggestion[2]))
                counter += 1
        # stop the annotator
        nlp.stop()
        return generated_facts
