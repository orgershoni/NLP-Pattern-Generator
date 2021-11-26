from hebrew_verbs_provider import create_verbs_table
from arabic_verbs_provider import load_verbs_from_json, ArabicTransformer
from typing import List
from utils import Language, Gender, Tense
from annotated_word import WordType, AnnotatedWord
import nodebox_linguistics_extended as nle
from replacments_db import *
from utils import *

class TenseLessRepsProvider:

    @classmethod
    def get_dictionary(cls, lang: Language):

        if lang == Language.HEBREW:
            return no_tense_words_hebrew
        if lang == Language.ENGLISH:
            return no_tense_words_english
        if lang == Language.ARABIC:
            return no_tense_words_arabic

        raise KeyError(f"{lang} is not fully supported in TenseLessRepsProvider")

    @classmethod
    def get_replacements(cls, word: str, gender: Gender, tense: Tense, lang: Language):
        d = TenseLessRepsProvider.get_dictionary(lang)
        return d[word][gender.value]

    @classmethod
    def has_replacements(cls, word: str, lang: Language):
        d = TenseLessRepsProvider.get_dictionary(lang)
        return word in d


class TenseFullRepsProvider:

    @classmethod
    def get_replacements(cls, word: str, gender: Gender, tense: Tense, lang: Language, verbs={}):
        if not verbs:
            if lang == Language.HEBREW:
                verbs_table = create_verbs_table("data/InflectedVerbsExtended.csv")
                verbs.update(verbs_table)
            if lang == Language.ARABIC:
                verbs = load_verbs_from_json()

        if lang == Language.HEBREW:
            if word in tense_full_hebrew:
                return tense_full_hebrew[word][tense.value][gender.value]
            return [verbs[word][tense.value][gender.value]]
        if lang == Language.ARABIC:
            if word in tense_full_arabic:
                return tense_full_arabic[word][tense.value][gender.value]
            return ArabicTransformer().reinflect(word, tense, gender)

        person = str(gender_to_person[gender])
        negate = word.endswith("n't")
        if tense == Tense.PAST:
            return [nle.verb.past(word, person=person, negate=negate)]
        elif tense == Tense.PRESENT:
            return [nle.verb.present(word, person=person, negate=negate)]
        else:
            if word == "didn't":
                return ["won't"]
            if word == "wasn't":
                return ["won't be"]
            return [f"will {nle.verb.infinitive(word)}"]

    @classmethod
    def has_replacements(cls, word: str, lang: Language, verbs={}):
        if not verbs:
            if lang == Language.HEBREW:
                verbs_table = create_verbs_table("data/InflectedVerbsExtended.csv")
                verbs.update(verbs_table)
            if lang == Language.ARABIC:
                verbs = load_verbs_from_json()

        if lang == Language.HEBREW:
            return word in tense_full_hebrew or word in verbs
        if lang == Language.ARABIC:
            return word in tense_full_arabic or word in verbs

        try:
            cls.get_replacements(word, Gender.HE, Tense.PAST, Language.ENGLISH)
            return True
        except KeyError:
            return False


def get_replacements(word: AnnotatedWord, gender: Gender, tense: Tense,
                     lang: Language) -> List[str]:
    if word.type == WordType.REGULAR:
        return [word.pattern]
    word = word.actual_word
    if TenseFullRepsProvider.has_replacements(word, lang):
        return TenseFullRepsProvider.get_replacements(word, gender, tense, lang)
    else:
        return TenseLessRepsProvider.get_replacements(word, gender, tense, lang)
