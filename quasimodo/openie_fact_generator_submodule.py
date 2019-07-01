import re
import inflect
import logging
from stanfordnlp.server import CoreNLPClient, AnnotationException, TimeoutException
import stanfordnlp.server.client
from nltk.corpus import wordnet as wn
import spacy

from quasimodo.openie_reader import OpenIEReader
from .multiple_scores import MultipleScore
from .generated_fact import GeneratedFact
from .statement_maker import StatementMaker
from .submodule_interface import SubmoduleInterface
from .modality import Modality
from .referencable_interface import ReferencableInterface
from quasimodo.parameters_reader import ParametersReader

PATTERN = 2

SCORE = 1

SUBJECT = 3

NEGATIVITY = 3

STATEMENT = 0

_nlp = spacy.load('en_core_web_sm')
_plural_engine = inflect.engine()

reference_corenlp = ReferencableInterface("CoreNLP")
reference_openie5 = ReferencableInterface("OpenIE5")

parameters_reader = ParametersReader()
memory_corenlp = parameters_reader.get_parameter("memory-corenlp") or "10G"


def _simple_extraction(sentence):
    tokens = []
    for token in _nlp(sentence):
        tokens.append(token.text.lower())
    if "can" in tokens:
        idx_can = tokens.index("can")
        if tokens[0] == "not":
            return [' '.join(tokens[1:idx_can]), "can", " ".join(tokens[idx_can + 1:]), True]
        return [' '.join(tokens[:idx_can]), "can", " ".join(tokens[idx_can+1:]), False]
    if len(tokens) == 2:
        return [tokens[0], "can", tokens[1], False]
    if len(tokens) == 3:
        synsets = wn.synsets(tokens[1])
        # We want a verb!
        for synset in synsets:
            if synset.pos() == "v":
                return [tokens[0], tokens[1], tokens[2], False]
    return None


def _try_extend(subj, pred, obj, sentence):
    # works for short sentences
    # But some problems with adjectives
    # eg african people have big nose and lips
    end = obj + " and "
    pos = sentence.find(end)
    if pos != -1:
        new_obj = sentence[pos + len(end):].strip()
        if " " not in new_obj:
            return subj, pred, new_obj
    return None


def start_corenlp_client():
    corenlp_client = CoreNLPClient(
        start_server=True,
        endpoint='http://localhost:9000',
        memory=memory_corenlp,
        threads=50,
        timeout=10000000,
        annotators=['openie'],
        output_format="json",
        properties={'annotators': 'openie',
                    'inputFormat': 'text',
                    'outputFormat': 'json',
                    'serializer': 'edu.stanford.nlp.pipeline.ProtobufAnnotationSerializer',
                    'openie.affinity_probability_cap': '1.0',
                    "openie.max_entailments_per_clause": "500"})
    corenlp_client.TIMEOUT = 100
    return corenlp_client


def remove_punctuation_from_suggestion(suggestion):
    return suggestion[STATEMENT].replace(".", "").replace("?", "").replace("!", "")


def join_sentences_from_batch(batch):
    sentences = " . ".join([remove_punctuation_from_suggestion(x) for x in batch]) + " . "
    return sentences


def replace_special_characters(sentence):
    replacements = [("-LRB-", "("), ("-RRB-", ")"), ("-LSB-", "["), ("-RSB-", "]"), ("-LCB-", "{"), ("-RCB-", "}"),
                    ("&amp;", "&")]
    for to_replace, replacement in replacements:
        sentence = sentence.replace(to_replace, replacement)
    return sentence


def annotate_sentences(corenlp_client, sentences, batch, batches):
    try:
        out = corenlp_client.annotate(sentences)
    except TimeoutException:
        logging.info("Timeout with: " + sentences)
        batches.append(batch)
        out = dict()
    except AnnotationException:
        logging.info("Annotation Error with: " + sentences)
        batches.append(batch)
        out = dict()
    except stanfordnlp.server.client.PermanentlyFailedException:
        logging.info("Permanent failed")
        corenlp_client.stop()
        corenlp_client = start_corenlp_client()
        batches.append(batch)
        out = dict()
    return corenlp_client, out


def get_statement_from_corenlp_sentence(sentence):
    return " ".join(filter(lambda x: x != ".", [x["word"] for x in sentence["tokens"]]))


def remove_empty_sentences(full_sentence):
    full_sentence = list(filter(lambda x: len(x[STATEMENT]) > 0, full_sentence))
    return full_sentence


def get_spo_from_triple(triple):
    subject = triple["subject"]
    obj = triple["object"]
    predicate = triple["relation"]
    return subject, predicate, obj


def get_position_subject(subject, suggestion):
    position_subject = suggestion[STATEMENT].find(subject)
    if suggestion[STATEMENT].find("a " + subject) != -1:
        position_subject = suggestion[STATEMENT].find("a " + subject)
    elif suggestion[STATEMENT].find("the " + subject) != -1:
        position_subject = suggestion[STATEMENT].find("the " + subject)
    return position_subject


def get_negativity(suggestion):
    negative = False
    if suggestion[PATTERN] is not None:
        negative = suggestion[PATTERN].is_negative()
    if suggestion[NEGATIVITY]:
        negative = True
    return negative


def contains_than_in_object(corenlp_result_sentence):
    contains_than = False
    for triple in corenlp_result_sentence["openie"]:
        obj = triple["object"]
        if " than " in obj:
            contains_than = True
    return contains_than


def get_number_words(maxi_obj):
    maxi_length_object = maxi_obj.count(" ") + 1
    return maxi_length_object


def get_maximal_object(corenlp_result_sentence, maxi_length_predicate):
    maxi_length_object = 1
    maxi_obj = ""
    for triple in corenlp_result_sentence["openie"]:
        predicate = triple["relation"]
        obj = triple["object"]
        if maxi_length_predicate == predicate.count(" ") + 1:
            if obj.count(" ") + 1 > maxi_length_object:
                maxi_length_object = get_number_words(obj)
                maxi_obj = obj
    return maxi_obj


def get_maximal_length_of_a_predicate(corenlp_result_sentence):
    maxi_length_predicate = 1
    for triple in corenlp_result_sentence["openie"]:
        predicate = triple["relation"]
        maxi_length_predicate = max(get_number_words(predicate),
                                    maxi_length_predicate)
    return maxi_length_predicate


def are_different_sentences(regex_no_alpha, statement_extracted_from_openie, suggestion):
    batch_and_current_sentence_do_not_match = regex_no_alpha.sub("", statement_extracted_from_openie) != \
                                              regex_no_alpha.sub("", suggestion[STATEMENT])
    return batch_and_current_sentence_do_not_match


def get_modality(subject, obj, maxi_length_object, maxi_obj, suggestion):
    modality_temp = ""
    if maxi_length_object != get_number_words(obj):
        modality_temp = "TBC[" + maxi_obj + "]"
    position_subject = get_position_subject(subject, suggestion)
    if position_subject != 0:
        if len(modality_temp) > 0:
            modality_temp += " // "
        modality = Modality(modality_temp + "some[subj" + "/" + suggestion[STATEMENT][:position_subject] + "]")
    else:
        modality = Modality(modality_temp)
    return modality


class OpenIEFactGeneratorSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self.statement_maker = StatementMaker()
        self._max_query_length = 99990
        self.default_number_suggestions = 8  # The maximum number of suggestions
        self._module_reference = module_reference
        self.regex_no_alpha = re.compile("[^a-zA-Z]")
        self.counter = 0

    def process(self, input_interface):
        raise NotImplementedError

    def _compute_batch_openie(self, suggestions):
        logging.info("Transformation questions to statement")
        full_sentence = self.get_all_batch_components_from_suggestions(suggestions)
        batches = self.get_batches_from_batch_components(full_sentence)
        return batches

    def get_all_batch_components_from_suggestions(self, suggestions):
        full_sentence = []
        for suggestion in suggestions:
            self.transforms_suggestion_into_batch_component(suggestion, full_sentence)
        full_sentence = remove_empty_sentences(full_sentence)
        return full_sentence

    def get_batches_from_batch_components(self, full_sentence):
        batches = []
        begin = 0
        counter = 0
        for i in range(len(full_sentence)):
            batch_size_is_too_long = counter + 3 + len(full_sentence[i][0]) > self._max_query_length
            if batch_size_is_too_long:
                batches.append(full_sentence[begin:i])
                begin = i
                counter = 0
            counter += len(full_sentence[i][0]) + 3
        batches.append(full_sentence[begin:])
        return batches

    def transforms_suggestion_into_batch_component(self, suggestion, full_sentence):
        # question to statement
        # We need this because of OpenIE very bad with questions
        new_sentence = self.statement_maker.to_statement(suggestion[STATEMENT],
                                                         suggestion[SUBJECT])
        if new_sentence[:6] == "there ":
            new_sentence = new_sentence[6:]
            new_sentence = self.statement_maker.to_statement("why " + new_sentence,
                                                             suggestion[SUBJECT])
        if " are not " in new_sentence:
            full_sentence.append((new_sentence.replace(" are not ", " are "),
                                  suggestion[SCORE],
                                  suggestion[PATTERN],
                                  True))
        elif " is not " in new_sentence[6:]:
            full_sentence.append((new_sentence.replace(" is not ", " is "),
                                  suggestion[SCORE],
                                  suggestion[PATTERN],
                                  True))
        elif new_sentence != "":
            negativity = False
            if "cannot" in suggestion[STATEMENT] or "can't" in suggestion[STATEMENT]:
                negativity = True
            full_sentence.append((new_sentence,
                                  suggestion[SCORE],
                                  suggestion[PATTERN],
                                  negativity))

    def get_generated_facts(self, suggestions):
        batches = self._compute_batch_openie(suggestions)
        corenlp_client = start_corenlp_client()

        generated_facts = []

        while batches:
            logging.info("%d batches remaining", len(batches))
            batch = batches.pop()
            # We annotate the sentence
            # And extract the triples
            sentences = join_sentences_from_batch(batch)
            corenlp_client, out = annotate_sentences(corenlp_client, sentences, batch, batches)
            self.counter = 0
            if "sentences" not in out:
                continue
            for corenlp_result_sentence in out["sentences"]:
                if self.counter >= len(batch):
                    logging.error("The counter and the batch do not match. Expected: %d, Received: %d",
                                  len(batch), self.counter)
                    break
                self.process_corenlp_result(corenlp_result_sentence, batch, generated_facts)
        # stop the annotator
        corenlp_client.stop()
        return generated_facts

    def process_corenlp_result(self, corenlp_result_sentence, batch, generated_facts):
        suggestion = batch[self.counter]
        if len(corenlp_result_sentence["tokens"]) == 0:
            self.counter += 1
            logging.debug("Empty sentence encountered")
            return
        statement_extracted_from_openie = get_statement_from_corenlp_sentence(corenlp_result_sentence)
        statement_extracted_from_openie = replace_special_characters(statement_extracted_from_openie)
        batch_and_current_sentence_do_not_match = are_different_sentences(self.regex_no_alpha,
                                                                          statement_extracted_from_openie,
                                                                          suggestion)
        if batch_and_current_sentence_do_not_match:
            logging.error("The subjects do not match. Received: %s,"
                          "Expecting: %s", statement_extracted_from_openie, suggestion)
            # Check if we went too fast
            suggestion = batch[self.counter - 1]
            previous_batch_and_sentence_do_not_match = are_different_sentences(
                self.regex_no_alpha,
                statement_extracted_from_openie,
                suggestion)
            if previous_batch_and_sentence_do_not_match:
                self.counter += 1
                return
            else:
                self.counter -= 1
        maxi_length_predicate = get_maximal_length_of_a_predicate(corenlp_result_sentence)
        maxi_obj = get_maximal_object(corenlp_result_sentence, maxi_length_predicate)
        maxi_length_object = get_number_words(maxi_obj)
        contains_than = contains_than_in_object(corenlp_result_sentence)
        score_based_on_ranking = (2 * self.default_number_suggestions - suggestion[1]) / \
                                 (2 * self.default_number_suggestions)
        if len(corenlp_result_sentence["openie"]) == 0:
            # Try simple extraction as OpenIE is bad for this
            se = _simple_extraction(suggestion[0])
            if se is not None:
                new_fact = self.get_fact_from_simple_extraction(se, score_based_on_ranking, suggestion)
                generated_facts.append(new_fact)
        for triple in corenlp_result_sentence["openie"]:
            self.process_triple(triple, suggestion, contains_than, generated_facts, maxi_length_object,
                                maxi_length_predicate, maxi_obj, score_based_on_ranking)
        self.counter += 1

    def process_triple(self, triple, suggestion, contains_than, generated_facts, maxi_length_object,
                       maxi_length_predicate, maxi_obj, score_based_on_ranking):
        subject, predicate, obj = get_spo_from_triple(triple)
        # This is to prevent too many extractions
        # If it useful in practice to extract more than one fact?
        if (maxi_length_predicate != get_number_words(predicate)) or \
                (maxi_length_object != get_number_words(obj) and contains_than):
            return
        negative = get_negativity(suggestion)
        modality = get_modality(subject, obj, maxi_length_object, maxi_obj, suggestion)
        self.add_facts_to_generated_facts(generated_facts, subject, predicate, obj, modality, negative,
                                          score_based_on_ranking, suggestion)
        spo = _try_extend(subject, predicate, obj, suggestion[STATEMENT])
        if spo is not None:
            subject, predicate, obj = spo
            modality = get_modality(subject, obj, maxi_length_object, maxi_obj, suggestion)
            self.add_facts_to_generated_facts(generated_facts, subject, predicate, obj, modality, negative,
                                              score_based_on_ranking, suggestion)

    def add_facts_to_generated_facts(self, generated_facts, subject, predicate, obj, modality, negative,
                                     score_based_on_ranking, suggestion):
        multiple_score = MultipleScore()
        multiple_score.add_score(1.0, self._module_reference, reference_corenlp)
        multiple_score.add_score(score_based_on_ranking, self._module_reference, self)
        new_fact_corenlp = GeneratedFact(subject, predicate, obj, modality, negative, multiple_score, suggestion[0],
                                         suggestion[2])
        generated_facts.append(new_fact_corenlp)

    def get_fact_from_simple_extraction(self, extraction, score, suggestion):
        negative = get_negativity(suggestion) or extraction[3]
        multiple_score = MultipleScore()
        multiple_score.add_score(score, self._module_reference, self)
        new_fact = GeneratedFact(
            extraction[0],
            extraction[1],
            extraction[2],
            None,
            negative,
            # For the score, inverse the ranking (higher is
            # better) and add the confidence of the triple
            multiple_score,
            suggestion[0],
            suggestion[2])
        return new_fact

    def _openie_from_file(self, suggestions):
        openie_reader = OpenIEReader()
        generated_facts = []
        new_suggestions = []
        for suggestion in suggestions:
            self.transforms_suggestion_into_batch_component(suggestion, new_suggestions)
        for suggestion in new_suggestions:
            sentence = suggestion[STATEMENT]
            facts = openie_reader.get_from_sentence(sentence)
            negative = get_negativity(suggestion)
            facts = [fact for fact in facts if len(fact) > 0 and len(fact[0]) > 1 and len(fact[1]) > 1 and len(fact[2]) > 1]
            for fact in facts:
                multiple_score = MultipleScore()
                multiple_score.add_score(float(fact[3].replace(",", ".")), self._module_reference, reference_openie5)
                generated_facts.append(
                    GeneratedFact(
                        fact[0],
                        fact[1],
                        fact[2],
                        "",
                        negative,
                        multiple_score,
                        sentence,
                        suggestion[2]))
        return generated_facts
