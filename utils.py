import nltk
from enum import Enum


def capitalize_first_letter(st: str):
    if not st:
        return st
    return st[0].upper() + st[1:]


def compute_bleu(ref,  translation):
    return nltk.translate.bleu_score.sentence_bleu([ref], translation)


class Language(Enum):
    ENGLISH = 1
    HEBREW = 2
