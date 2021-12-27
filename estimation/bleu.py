from typing import List
from utils import GeneratedSentence, compute_bleu
import numpy as np

def bleu(actual_lines : List[str] , expected_lines : List[str] ):
    bleu_scores = []
    for translated_sent, sent_ref in zip(actual_lines, expected_lines):
        bleu_scores.append(compute_bleu(sent_ref, translated_sent))
    return bleu_scores


def patterns_bleu(per_pattern_sentences):
    import numpy as np
    for pattern_info in per_pattern_sentences:
        bleu_scores = np.array(bleu(pattern_info['actual_sentences'], pattern_info['expected_sentences']))
        pattern_info['max_bleu'] = bleu_scores.max()
        pattern_info['argmax_bleu'] = bleu_scores.argmax()
        pattern_info['mean_bleu'] = bleu_scores.mean()

    return per_pattern_sentences
