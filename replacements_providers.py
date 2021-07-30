from hebrew_verbs_provider import create_verbs_table
from typing import List
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


class TenseLessRepsProvider:

    @classmethod
    def get_replacements(cls, word, gender, tense, lang):
        d = no_tense_words_hebrew if lang == "hebrew" else no_tense_words_english
        return d[word][gender]

    @classmethod
    def has_replacements(cls, word, lang):
        d = no_tense_words_hebrew if lang == "hebrew" else no_tense_words_english
        return word in d

import nodebox_linguistics_extended as nle

def person_from_gender(gender: str):
    if gender == "He" or gender == "She":
        return '3'
    if gender == 'I' or gender == 'We':
        return '1'
    return '2'

class TenseFullRepsProvider:

    @classmethod
    def get_replacements(cls, word, gender, tense, lang, verbs={}):
        if not verbs:
            verbs_table = create_verbs_table(r"C:\Users\omryg\Downloads\InflectedVerbsExtended.csv")
            verbs.update(verbs_table)

        if lang == "hebrew":
            if word in tense_full_hebrew:
                return tense_full_hebrew[word][tense][gender]
            return [verbs[word][tense][gender]]
        person = person_from_gender(gender)
        negate = word.endswith("n't")
        if tense == "PAST":
            return [nle.verb.past(word, person=person, negate=negate)]
        return [nle.verb.present(word, person=person, negate=negate)]

    @classmethod
    def has_replacements(cls, word, lang, verbs={}):
        if not verbs:
            verbs_table = create_verbs_table(r"C:\Users\omryg\Downloads\InflectedVerbsExtended.csv")
            verbs.update(verbs_table)

        if lang == "hebrew":
            return word in tense_full_hebrew or word in verbs
        try:
            cls.get_replacements(word, "He", "PAST", "english")
            return True
        except KeyError:
            return False


def get_replacements(word, gender, tense, lang) -> List[str]:
    if word.type == "REGULAR_WORD":
        return [word.content]
    word = word.role
    if TenseFullRepsProvider.has_replacements(word, lang):
        return TenseFullRepsProvider.get_replacements(word, gender, tense, lang)
    else:
        return TenseLessRepsProvider.get_replacements(word, gender, tense, lang)
