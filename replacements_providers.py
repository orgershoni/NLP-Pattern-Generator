from hebrew_verbs_provider import create_verbs_table
from typing import List
from utils import Language, Gender, Tense
from annotated_word import WordType, AnnotatedWord
import nodebox_linguistics_extended as nle


no_tense_words_hebrew = {
    "מירב": {
        "He": [],
        "She": ["דנה", "מירב"],
        "We": [],
        "I_F": [],
        "I_M": [],
    },
    "יובל": {
        "He": ["מיכאל", "עמוס"],
        "She": ["ירדן", "ענבר"],
        "We": [],
        "I_M": ["מיכאל", "עמוס"],
        "I_F": ["ירדן", "ענבר"],
    },
    "עמוס": {
        "He": ["מיכאל", "עמוס"],
        "We": [],
        "She": [],
        "I_M": [],
        "I_F": []
    },
    "ו": {
        "He": ["ו"],
        "We": ["נו"],
        "She": ["ה"],
        "I_M": ["י"],
        "I_F": ["י"],
    },
    "בנו": {
        "He": ["בנו"],
        "She": ["בנה"],
        "I_M": ["בני"],
        "I_F": ["בני"],
        "We_M": ["בננו"]
    },
    "שלו": {
        "I_M": ["שלי"],
        "I_F": ["שלי"],
        "She": ["שלה"],
        "We_M": ["שלנו"],
        "We_F": ["שלנו"],
        "He": ["שלו"]
    },
    "ממנו": {
        "I_M": ["ממני"],
        "I_F": ["ממני"],
        "She": ["ממנה"],
        "He": ["ממנו"],
        "We": ["מאיתנו"],
    },
    "למישהו": {
        "I_F": ["לי"],
        "I_M": ["לי"],
        "She": ["לה", "לאישה", "למירב"],
        "He": ["לו", "לילד", "לעמרי"],
        "We": ["לנו", "לנו"],
    },
    "עםמישהו": {
        "I_F": ["איתי"],
        "I_M": ["איתי"],
        "She": ["איתה", "עם האישי", "עם מירב"],
        "He": ["איתו", "עם הילד", "עם עמרי"],
        "We": ["איתנו", "איתנו"],
    },
    "לו": {
        "I_M": ["לי"],
        "I_F": ["לי"],
        "She": ["לה"],
        "We": ["לנו"],
        "He": ["לו"]
    },
    "לעצמו":
        {
        "I_F": ["לעצמי"],
        "I_M": ["לעצמי"],
        "She": ["לעצמה"],
        "We": ["לעצמנו"],
        "He": ["לעצמו"]
        },
    "הוא": {
        "She": ["היא"],
        "He": ["הוא"],
        "We": ["אנחנו", "אנו"],
        "I_F": ["אני"],
        "I_M": ["אני"]
    },
    "מישהו": {
        "She": ["היא", "האישה", "מירב"],
        "He": ["הוא", "הילד", "עמרי"],
        "We": ["אנחנו", "אנו"],
        "I_M": ["אני"],
        "I_F": ["אני"]
    },
    "שלמישהו": {
        "She": ["שלה", "של האישה", "של מירב"],
        "He": ["שלו", "של הילד", "של עמרי"],
        "We": ["שלנו", "שלנו"],
        "I_F": ["שלי"],
        "I_M": ["שלי"]
    }
}

no_tense_words_english = {
    "Amos": {
        "He": ["Michael", "Amos"],
        "We": [],
        "She": [],
        "I_M": [],
        "I_F": []
    },
    "Yuval": {
        "He": ["Michael", "Amos"],
        "She": ["Yarden", "Inbar"],
        "We": [],
        "I_M": ["Michael", "Amos"],
        "I_F": ["Yarden", "Inbar"]
    },
    "someone":
        {
            "She": ["she", "the woman", "Meirav"],
            "He": ["he", "the child", "Omry"],
            "We": ["we", "we"],
            "I_F": ["I"],
            "I_M": ["I"]
        },
    "tosomeone": {
        "I_F": ["to me"],
        "I_M": ["to me"],
        "She": ["to her", "to the woman", "to Meirav"],
        "He": ["to him", "to the child", "to Omry"],
        "We": ["to us", "to us"],
    },
    "someoneobj": {
        "I_F": ["me"],
        "I_M": ["me"],
        "She": ["her", "the woman", "Meirav"],
        "He": ["him", "the child", "Omry"],
        "We": ["us", "us"],
    },
    "he":
        {
            "She": ["she"],
            "He": ["he"],
            "We": ["we", "we"],
            "I_M": ["I"],
            "I_F": ["I"]
        },
    "his":
        {
            "She": ["her"],
            "He": ["his"],
            "We": ["our"],
            "I_F": ["my"],
            "I_M": ["my"]
        },
    "him":
        {
            "She": ["her"],
            "He": ["him"],
            "We": ["us"],
            "I_M": ["me"],
            "I_F": ["me"]
        },
    "himself":
        {
            "She": ["herself"],
            "He": ["himself"],
            "We": ["ourselves"],
            "I_M": ["myself"],
            "I_F": ["myself"]
        },
    "someone's": {
        "She": ["her", "the woman's", "Meirav's"],
        "He": ["his", "the child's", "Omry's"],
        "We": ["our", "our"],
        "I_M": ["my"],
        "I_F": ["my"],
    },
    "Meirav": {
        "He": [],
        "She": ["Dana", "Meirav"],
        "We": [],
        "I_F": [],
        "I_M": []
    }
}
tense_full_english = {
}

tense_full_hebrew = {
"היהה": {
        "PRESENT": {
            "She": [""],
            "He": [""],
            "We": [""],
            "I_M": [""],
            "I_F": [""]
        },
        "PAST": {
            "She": ["היה"],
            "He": ["היה"],
            "We": ["היה"],
            "I_M": ["היה"]
            , "I_F": ["היה"]
        },
    },
"נטה": {
        "PRESENT": {
            "She": ["נוטה"],
            "He": ["נוטה"],
            "We": ["נוטים"],
            "I_M": ["נוטה"],
            "I_F": ["נוטה"]
        },
        "PAST": {
            "She": ["נטתה"],
            "He": ["נטה"],
            "We": ["נטינו"],
            "I_F": ["נטיתי"],
            "I_M": ["נטיתי"]
        },
    },
"אין": {
        "PRESENT": {
            "She": ["אין"],
            "He": ["אין"],
            "We": ["אין"],
            "I_M": ["אין"],
            "I_F": ["אין"]
        },
        "PAST": {
            "She": ["לא היה"],
            "He": ["לא היה"],
            "We": ["לא היה"],
            "I_M": ["לא היה"]
            , "I_F": ["לא היה"]
        },
    },
}

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


class TenseLessRepsProvider:

    @classmethod
    def get_replacements(cls, word: str, gender: Gender, tense: Tense, lang: Language):
        d = no_tense_words_hebrew if lang == Language.HEBREW else no_tense_words_english
        return d[word][gender.value]

    @classmethod
    def has_replacements(cls, word: str, lang: Language):
        d = no_tense_words_hebrew if lang == Language.HEBREW else no_tense_words_english
        return word in d


class TenseFullRepsProvider:

    @classmethod
    def get_replacements(cls, word: str, gender: Gender, tense: Tense, lang: Language, verbs={}):
        if not verbs:
            verbs_table = create_verbs_table("data/InflectedVerbsExtended.csv")
            verbs.update(verbs_table)

        if lang == Language.HEBREW:
            if word in tense_full_hebrew:
                return tense_full_hebrew[word][tense.value][gender.value]
            return [verbs[word][tense.value][gender.value]]
        person = str(gender_to_person[gender])
        negate = word.endswith("n't")
        if tense == Tense.PAST:
            return [nle.verb.past(word, person=person, negate=negate)]
        return [nle.verb.present(word, person=person, negate=negate)]

    @classmethod
    def has_replacements(cls, word: str, lang: Language, verbs={}):
        if not verbs:
            verbs_table = create_verbs_table("data/InflectedVerbsExtended.csv")
            verbs.update(verbs_table)

        if lang == Language.HEBREW:
            return word in tense_full_hebrew or word in verbs
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
