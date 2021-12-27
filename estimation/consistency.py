import distance
from typing import List, Dict

from populate_patterns.general.patterns_populator_ng import tokenize

def words_levenshtein(sent1 : str, sent2 : str) -> int:

    words1 = words(sent1)
    words2 = words(sent2)
    return distance.levenshtein(words1, words2)

def get_embbeded_leven_dist(pattern : str):
    tokens = tokenize(pattern)
    distance = 0
    # print(tokens)
    for token in tokens:
        if token.startswith("#"):
            distance += 1
    return distance   

def words(string : str):
    return string.split(' ')

def costum_levenshtein(sent1 : str, sent2 : str, ref1 : str, ref2 : str):
    """
    This function computes the levenshtein distance between 2 sentences.
    Then, reduce for this amount the levenshtein distance between their sytethic refrences
    Finally return the normalized distance (by the longest sentence)
    """
    leven_dist = max(words_levenshtein(sent1, sent2) - words_levenshtein(ref1, ref2), 0)
    normlization_factor = max(len(words(sent1)), len(words(sent2)))
    return leven_dist / normlization_factor

def generate_leven_pairs(pattern_info):

    reference_idx = pattern_info['argmax_bleu']
    actual_ref = pattern_info['actual_sentences'][reference_idx]
    expected_ref = pattern_info['expected_sentences'][reference_idx]
    pairs = []
    for i, sentence in enumerate(pattern_info['actual_sentences']):
        if i != reference_idx:
            pairs.append((sentence, actual_ref, pattern_info['expected_sentences'][i], expected_ref))
    return pairs

def patterns_levenshtein(clustered_sentences : List[Dict]):
    import numpy as np
    import pandas as pd
    data = {'Sentence 1' : [],
            'Sentence 2' : [],
            'Levenshtein score' : []}
    for pattern_info in clustered_sentences:
        leven_pairs = generate_leven_pairs(pattern_info)
        scores = []
        for pair_data in leven_pairs:
            sent1, sent2,_, _ = pair_data
            leven_dist = costum_levenshtein(*pair_data)
            scores.append(leven_dist)

            data['Sentence 1'].append(sent1)
            data['Sentence 2'].append(sent2)
            data['Levenshtein score'].append(leven_dist)
        scores = np.array(scores)
        pattern_info['mean_leven'] = scores.mean()
        pattern_info['min_leven'] = scores.min()
        pattern_info['max_leven'] = scores.max()

        data['Sentence 1'].append('#')
        data['Sentence 2'].append('#')
        data['Levenshtein score'].append('#')

    pd.DataFrame.from_dict(data).to_csv('outputs/levenshtein_scores.csv', encoding="utf-8")
    return clustered_sentences

