import distance
from typing import List
from populate_patterns.general.patterns_populator_ng import tokenize
from utils import GeneratedSentence, all_pairs

def levenshtein(sent1 : str, sent2 : str) -> int:

    list1 = sent1.split(' ')
    list2 = sent2.split(' ')
    return distance.levenshtein(list1, list2)

def get_basic_distance(pattern : str):
    tokens = tokenize(pattern)
    distance = 0
    # print(tokens)
    for token in tokens:
        if token.startswith("#"):
            distance += 1
    return distance

def patterns_levenshtein(actual_translations : List[str], reference_translations : List[GeneratedSentence]):
    import numpy as np

    # TODO : Maybe move this to a different function
    
    # cluster actual translations into groups of same pattern
    per_pattern_sentences = {}
    for actual, expected in zip(actual_translations, reference_translations):
        if not expected.origin_pattern in per_pattern_sentences.keys():
            per_pattern_sentences[expected.origin_pattern] = {}
            base_distance = get_basic_distance(expected.origin_pattern)
            per_pattern_sentences[expected.origin_pattern]['base_dist'] = base_distance
            per_pattern_sentences[expected.origin_pattern]['sentences'] = list()
        
        per_pattern_sentences[expected.origin_pattern]['sentences'].append(actual)
    
    for raw_pattern, pattern_dict in per_pattern_sentences.items():
        base_distance = pattern_dict['base_dist']
        actual_pairs = all_pairs(pattern_dict['sentences'])
        scores = []
        for sent1, sent2 in actual_pairs:
            leven_dist = max(levenshtein(sent1, sent2) - base_distance, 0) #explain why it can be negative
            scores.append(leven_dist)
        
        per_pattern_sentences[raw_pattern]['leven'] = np.array(scores).mean()

        print("Pattern {0} || leven score is {1}".format(raw_pattern, per_pattern_sentences[raw_pattern]['leven']))    