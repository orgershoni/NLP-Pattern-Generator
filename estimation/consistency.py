import distance
from typing import List
from populate_patterns.general.patterns_populator_ng import tokenize
from utils import GeneratedSentence

def levenshtein(sent1 : str, sent2 : str) -> int:

    list1 = sent1.split(' ')
    list2 = sent2.split(' ')
    print(f"sent1: {sent1}")
    print(f"sent2: {sent2}")
    return distance.levenshtein(list1, list2)

def get_basic_distance(pattern : str):
    tokens = tokenize(pattern)
    distance = 0
    print(tokens)
    for token in tokens:
        if token.startswith("#"):
            distance += 1
    return distance

def patterns_levenshtein(actual_translations : List[str], reference_translations : List[GeneratedSentence]):

    per_pattern_sentences = {}
    for actual, expected in zip(actual_translations, reference_translations):
        if not expected.origin_pattern in per_pattern_sentences.keys():
            per_pattern_sentences[expected.origin_pattern] = list()
        
        per_pattern_sentences[expected.origin_pattern].append((actual, expected))
    
    for pattern_sentences in per_pattern_sentences.values():
        for actual, expected in pattern_sentences:
            base_distance = get_basic_distance(expected.origin_pattern)
            x = levenshtein(actual, expected.sentence) - base_distance
            print(f"Leven score {x}")
    