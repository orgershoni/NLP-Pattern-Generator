import distance
from typing import List, Dict

from populate_patterns.general.patterns_populator_ng import tokenize
from utils import all_pairs

def levenshtein(sent1 : str, sent2 : str) -> int:

    list1 = sent1.split(' ')
    list2 = sent2.split(' ')
    return distance.levenshtein(list1, list2)

def get_embbeded_leven_dist(pattern : str):
    tokens = tokenize(pattern)
    distance = 0
    # print(tokens)
    for token in tokens:
        if token.startswith("#"):
            distance += 1
    return distance   

def patterns_levenshtein(clustered_sentences : List[Dict]):
    import numpy as np
    for pattern_info in clustered_sentences:
        base_distance = get_embbeded_leven_dist(pattern_info['dest_pattern'])
        sentences_pairs = all_pairs(pattern_info['actual_sentences'])
        scores = []
        for sent1, sent2 in sentences_pairs:
            leven_dist = max(levenshtein(sent1, sent2) - base_distance, 0) #explain why it can be negative
            scores.append(leven_dist)
        pattern_info['levenstein_score'] = np.array(scores).mean()
    return clustered_sentences

