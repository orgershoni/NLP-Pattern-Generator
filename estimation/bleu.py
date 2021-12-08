from typing import List
from utils import compute_bleu

def bleu(actual_lines : List[str] , expected_lines : List[str] ):
    bleu_scores = []
    for translated_sent, sent_ref in zip(actual_lines, expected_lines):
        bleu_scores.append(compute_bleu(sent_ref, translated_sent))
    return bleu_scores