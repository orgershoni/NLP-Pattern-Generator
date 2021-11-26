import nltk
from enum import Enum


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