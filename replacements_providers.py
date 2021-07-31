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
        "I": ["דנה", "מירב"]
    },
    "יובל": {
        "He": ["מיכאל", "עמוס"],
        "She": ["ירדן", "ענבר"],
        "We": [],
        "I": ["מיכאל", "עמוס"]
    },
    "עמוס": {
        "He": ["מיכאל", "עמוס"],
        "We": [],
        "She": [],
        "I": []#["מיכאל", "עמוס"]
    },
    "ו": {
        "He": ["ו"],
        "We": ["נו"],
        "She": ["ה"],
        "I": ["י"]
    },
    "צלחתה": {
        "He": ["צלחתו"],
        "She": ["צלחתה"],
        "We": ["צלחתנו"],
        "I": ["צלחתי"]
    },
    "בנו": {
        "He": ["בנו"],
        "She": ["בנה"],
        "I": ["בני"],
        "We": ["בננו"]
    },
    "שלו": {
        "I": ["שלי"],
        "She": ["שלה"],
        "We": ["שלנו"],
        "He": ["שלו"]
    },
    "ממנו": {
        "I": ["ממני"],
        "She": ["ממנה"],
        "He": ["ממנו"],
        "We": ["מאיתנו"],
    },
    "למישהו": {
        "I": ["לי"],
        "She": ["לה", "לאישה", "למירב"],
        "He": ["לו", "לילד", "לעמרי"],
        "We": ["לנו", "לנו"],
    },
    "לו": {
        "I": ["לי"],
        "She": ["לה"],
        "We": ["לנו"],
        "He": ["לו"]
    },
    "לעצמו":
        {
        "I": ["לעצמי"],
        "She": ["לעצמה"],
        "We": ["לעצמנו"],
        "He": ["לעצמו"]
        },
    "הוא": {
        "She": ["היא"],
        "He": ["הוא"],
        "We": ["אנחנו", "אנו"],
        "I": ["אני"]
    },
    "מישהו": {
        "She": ["היא", "האישה", "מירב"],
        "He": ["הוא", "הילד", "עמרי"],
        "We": ["אנחנו", "אנו"],
        "I": ["אני"]
    },
    "שלמישהו": {
        "She": ["שלה", "של האישה", "של מירב"],
        "He": ["שלו", "של הילד", "של עמרי"],
        "We": ["שלנו", "שלנו"],
        "I": ["שלי"]
    }
}

no_tense_words_english = {
    "Amos": {
        "He": ["Michael", "Amos"],
        "We": [],
        "She": [],
        "I": []#["Michael", "Amos"]
    },
    "Yuval": {
        "He": ["Michael", "Amos"],
        "She": ["Yarden", "Inbar"],
        "We": [],
        "I": ["Michael", "Amos"]
    },
    "someone":
        {
            "She": ["she", "the woman", "Meirav"],
            "He": ["he", "the child", "Omry"],
            "We": ["we", "we"],
            "I": ["I"]
        },
    "tosomeone": {
        "I": ["me"],
        "She": ["her", "the woman", "Meirav"],
        "He": ["him", "the child", "Omry"],
        "We": ["us", "us"],
    },
    "he":
        {
            "She": ["she"],
            "He": ["he"],
            "We": ["we", "we"],
            "I": ["I"]
        },
    "his":
        {
            "She": ["her"],
            "He": ["his"],
            "We": ["our"],
            "I": ["my"]
        },
    "him":
        {
            "She": ["her"],
            "He": ["him"],
            "We": ["us"],
            "I": ["me"]
        },
    "himself":
        {
            "She": ["herself"],
            "He": ["himself"],
            "We": ["ourselves"],
            "I": ["myself"]
        },
    "someone's": {
        "She": ["her", "the woman's", "Meirav's"],
        "He": ["his", "the child's", "Omry's"],
        "We": ["our", "our"],
        "I": ["my"]
    },
    "Meirav": {
        "He": [],
        "She": ["Dana", "Meirav"],
        "We": [],
        "I": ["Dana", "Meirav"]
    }
}
from collections import defaultdict
tense_full_english = {
    "went": {
        "PRESENT": {
            "She": {"goes"},
            "He": {"goes"},
            "We": {"go"},
            "I": {"go"}
        },
        "PAST": {
            "She": {"went"},
            "He": {"went"},
            "We": {"went"},
            "I": {"went"}
        },
    },
    "didn't": {
        "PRESENT": {
            "She": {"doesn't"},
            "He": {"doesn't"},
            "We": {"don't"},
            "I": {"don't"}
        },
        "PAST": {
            "She": ["didn't"], "He": ["didn't"], "We": ["didn't"], "I": ["didn't"]
        }
    },
    "deserved": {
        "PRESENT": {
            "She": {"deserves"},
            "He": {"deserves"},
            "We": {"deserve"},
            "I": {"deserve"}
        },
    },
    "tended": {
        "PRESENT": {
            "She": {"tends"},
            "He": {"tends"},
            "We": {"tend"},
            "I": {"tend"}
        },
    },
    "was":
        {
            "PRESENT": {
                "She": ["is"],
                "He": ["is"],
                "We": ["are"],
                "I": ["am"]
            },
            "PAST": {
                "She": ["was"],
                "He": ["was"],
                "We": ["were"],
                "I": ["was"]
            }
        },
    "read": {
        "PRESENT": {
            "She": ["reads"],
            "He": ["reads"],
            "We": ["read"],
            "I": ["read"]
        },
    },

}

tense_full_hebrew = {
"היהה": {
        "PRESENT": {
            "She": [""],
            "He": [""],
            "We": [""],
            "I": [""]
        },
        "PAST": {
            "She": ["היה"],
            "He": ["היה"],
            "We": ["היה"],
            "I": ["היה"]
        },
    },
"נטה": {
        "PRESENT": {
            "She": ["נוטה"],
            "He": ["נוטה"],
            "We": ["נוטים"],
            "I": ["נוטה"]
        },
        "PAST": {
            "She": ["נטתה"],
            "He": ["נטה"],
            "We": ["נטינו"],
            "I": ["נטיתי"]
        },
    },
"אין": {
        "PRESENT": {
            "She": ["אין"],
            "He": ["אין"],
            "We": ["אין"],
            "I": ["אין"]
        },
        "PAST": {
            "She": ["לא היה"],
            "He": ["לא היה"],
            "We": ["לא היה"],
            "I": ["לא היה"]
        },
    },
}

gender_to_person = {
    Gender.HE: 3,
    Gender.SHE: 3,
    Gender.THEY: 3,
    Gender.II: 1,
    Gender.WE: 1,
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
