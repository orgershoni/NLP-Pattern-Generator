import nltk
from enum import Enum
from typing import List, Any

def capitalize_first_letter(st: str):
    if not st:
        return st
    return st[0].upper() + st[1:]


def compute_bleu(ref, translation):
    return nltk.translate.bleu_score.sentence_bleu([ref], translation)

class Language(Enum):
    ENGLISH = 1
    HEBREW = 2
    FRENCH = 3
    ARABIC = 4


class Gender(Enum):
    HE = "He"
    SHE = "She"
    WE_F = "WE_F"
    WE_M = "WE_M"
    THEY = "They"
    I_F = "I_F"
    I_M = "I_M"
    YOU = "You"


class Tense(Enum):
    PAST = "PAST"
    PRESENT = "PRESENT"
    FUTURE = "FUTURE"


class GeneratedSentence:
    def __init__(self, sentence : str, dest_pattern : str, src_pattern) -> None:
        self.sentence = sentence
        self.dest_pattern = dest_pattern
        self.src_pattern = src_pattern
    
    def pattern_uid(self):
        return self.dest_pattern + self.src_pattern


gender_to_person = {
    Gender.HE: 3,
    Gender.SHE: 3,
    Gender.THEY: 3,
    Gender.I_F: 1,
    Gender.I_M: 1,
    Gender.WE_F: 1,
    Gender.WE_M: 1,
    Gender.YOU: 2
}

def is_gender_plural(gender : Gender):

    return gender == Gender.WE_M or\
           gender == Gender.WE_F or\
           gender == Gender.THEY

def encode_arabic(arabic_txt : str):
    # install: pip install --upgrade arabic-reshaper
    import arabic_reshaper

    # install: pip install python-bidi
    from bidi.algorithm import get_display

    reshaped_text = arabic_reshaper.reshape(arabic_txt)    # correct its shape
    return get_display(reshaped_text)           # correct its direction

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

def lower_all(srcs : List[str]):

    return [src.lower() for src in srcs]

def all_pairs(src : List[Any]):
    from itertools import combinations
    return list(combinations(src, 2))


def cluster_by_pattern(actual_translations : List[str], reference_translations : List[GeneratedSentence]):
    per_pattern_sentences = {}
    for actual, expected in zip(actual_translations, reference_translations):
        if not expected.pattern_uid() in per_pattern_sentences.keys():
            pattern_info = {'dest_pattern' : expected.dest_pattern}
            pattern_info['src_pattern'] = expected.src_pattern
            pattern_info['actual_sentences'] = list()
            pattern_info['expected_sentences'] = list()
            per_pattern_sentences[expected.pattern_uid()] = pattern_info

        
        per_pattern_sentences[expected.pattern_uid()]['actual_sentences'].append(actual)
        per_pattern_sentences[expected.pattern_uid()]['expected_sentences'].append(expected.sentence)

    
    return [pattern_info for pattern_info in per_pattern_sentences.values()]
 