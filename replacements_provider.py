import re
from typing import Dict, List
from annotated_word import Word
from collections import defaultdict


def remove_diacritics(word):
    return re.sub("[\u0590-\u05CF]", "", word)


def get_tense(verb_attrs: List[str]):
    if "PAST" in verb_attrs:
        return "PAST"
    if "FUTURE" in verb_attrs:
        return "FUTURE"
    if "PRESENT" in verb_attrs:
        return "PRESENT"
    return ""


def get_gender(verb_attrs: List[str]):
    if "F" in verb_attrs and "SINGULAR" in verb_attrs and "THIRD" in verb_attrs:
        return "She"
    if "M" in verb_attrs and "SINGULAR" in verb_attrs and "THIRD" in verb_attrs:
        return "He"
    if "FIRST" in verb_attrs and "SINGULAR" in verb_attrs:
        return "I"
    if "FIRST" in verb_attrs and "PLURAL" in verb_attrs:
        return "We"
    return ""


def add_verb_record(record: str, verbs: Dict):
    attrs = remove_diacritics(record).split(",")
    verb = attrs[-1]
    content = attrs[2]
    metadata = attrs[3].split("+")
    if verb not in verbs:
        verbs[verb] = defaultdict(defaultdict)

    verb_record = verbs[verb]
    tense = get_tense(metadata)
    gender = get_gender(metadata)
    if not tense or not gender:
        return
    verb_record[tense][gender] = content


def create_verbs_table(verbs_table_path: str):
    from pathlib import Path
    data = Path(verbs_table_path).read_text(encoding="utf-8")
    lines = list(data.splitlines())[1:]
    verbs = {}
    for line in lines:
        add_verb_record(line, verbs)
    return verbs


def get_word_replacements_hebrew(word:Word, gender, tense, verbs={}):
    if not verbs:
        verbs_table = create_verbs_table(r"C:\Users\omryg\Downloads\InflectedVerbsExtended.csv")
        verbs.update(verbs_table)

    PLACES = ["מכולת", "קולנוע", "בית הספר", "מסעדה"]

    HI = "היא"
    HALCHA = "הלכה"
    LA = "לה"
    SHELA = "שלה"
    if word.type == "REGULAR_WORD":
        return {word.content}
    word = word.role
    HI_FEMALE_REP =["היא", "מירב", "האישה"]
    d = {
        "מירב": {
            "PRESENT": {
                "He": [],
                "She": ["מירב", "דנה"],
                "We": [],
                "I": ["מירב"]
            }
        },
        "מקום":
            {
              "PRESENT": {
                "I": PLACES,
                  "She": PLACES,
                  "He": PLACES,
                  "We": PLACES
              }

            },
        "יובל": {
            "PRESENT": {
                "He": ["עמוס", "מיכאל"],
                "She": ["ירדן", "ענבר"],
                "We": [],
                "I": ["עמרי"]
            }
        },
        "עמוס": {
            "PRESENT": {
                "He": ["עמוס", "מיכאל"],
                "We": [],
                "She": [],
                "I": []
            }
        },
        "ו": {
            "PRESENT": {
                "He": ["ו"],
                "We": ["נו"],
                "She": ["ה"],
                "I": ["י"]
            }
        },
        "צלחתה": {
            "PRESENT": {
                "He": ["צלחתו"],
                "She": ["צלחתה"],
                "We": ["צלחתנו"],
                "I": ["צלחתי"]
            }
        },
        "בנו": {
            "PRESENT":
                {
                    "He": ["בנו"],
                    "She": ["בנה"],
                    "I": ["בני"],
                    "We": ["בננו"]
                }
        },
        "שלו": {
            "PRESENT":
                {
                    "I": ["שלי"],
                    "She": ["שלה"],
                    "We": ["שלנו"],
                    "He": ["שלו"]
                }
        },
        "לו": {
            "PRESENT":
                {
                    "I": ["לי"],
                    "She": ["לה", "למירב", "לאישה"],
                    "We": ["לנו", "לנו"],
                    "He": ["לו","לילד" , "לעמרי"]
                }
        },
        "לוממש": {
            "PRESENT":
                {
                    "I": ["לי"],
                    "She": ["לה"],
                    "We": ["לנו"],
                    "He": ["לו"]
                }
        },
        "הוא": {
            "PRESENT": {
                    "She": HI_FEMALE_REP,
                    "He": ["הוא", "הילד", "עמרי"],
                    "We": ["אנחנו", "אנו"],
                    "I": ["אני"]
                    },
            "PAST": {
                "She": HI_FEMALE_REP,
                "He": {"הוא", "הילד", "עמרי"},
                "We": {"אנחנו", "אנו"},
                "I": {"אני"}
            }
        },
        "הואממש": {
            "PRESENT": {
                "She": {"היא"},
                "He": {"הוא"},
                "We": {"אנחנו"},
                "I": {"אני"}
            }
        },
        "שלוממש": {
            "PRESENT": {
            "She": {"שלה"},
            "He": {"שלו"},
            "I": {"שלי"},
            "We": {"שלנו"}
            }
        },
        "הלך": {
            "PRESENT": {
                "She": {"הולכת"},
                "He": {"הולך"},
                "We": {"הולכים"},
                "I": {"הולך"}
            },
        },
        "אמר": {
            "PRESENT": {
                "She": {"אומרת"},
                "He": {"אומר"},
                "We": {"אומרים"},
                "I": {"אומר"}
            },
            },
            "הקריא": {
                "PRESENT": {
                    "She": {"מקריאה"},
                    "He": {"מקריא"},
                    "We": {"מקריאים"},
                    "I": {"מקריא"}
                }
            },
        "הכין": {
            "PRESENT": {
                "She": {"מכינה"},
                "He": {"מכין"},
                "We": {"מכינים"},
                "I": {"מכין"}
            }
        },
        "רצה": {
            "PRESENT": {
                "She": {"רוצה"},
                "He": {"רוצה"},
                "We": {"רוצים"},
                "I": {"רוצה"}
            }
        },
        "שליובל": {
            "PRESENT": {
                "She": ["של מירב", "של ענבר", "שלה"],
                "He": ["של מיכאל", "של עמוס", "שלו"],
                "We": ["שלנו"],
                "I": ["שלי"]
            }
        },
        "ליובל": {
            "PRESENT": {
                "She": ["למירב", "לענבר", "לה"],
                "He": ["למיכאל", "לעמוס", "לו"],
                "We": ["לנו"],
                "I": ["לי"]
            }
        }

    }
    assert word in d or word in verbs, word
    if word in d:
        return d[word][tense][gender]
    return [verbs[word][tense][gender]]


def get_word_replacements_english(word:Word, gender, tense, verbs={}):

    if word.type == "REGULAR_WORD":
        return {word.content}
    word = word.role
    d = {
        "went": {
            "PRESENT": {
                "She": {"goes"},
                "He": {"goes"},
                "We": {"go"},
                "I": {"go"}
            },
        },
        "deserved": {
            "PRESENT": {
                "She": {"deserves"},
                "He": {"deserves"},
                "We": {"deserve"},
                "I": {"deserve"}
            },
        },
        "Yuval": {
            "PRESENT": {
                "He": ["Amos", "Michael"],
                "She": ["Yarden", "Inbar"],
                "We": [],
                "I": ["Omry"]
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
        "he":
            {
                "PRESENT": {
                    "She": ["She", "Meirav", "The woman"],
                    "He": ["He", "The Child", "Omry"],
                    "We": ["We", "We"],
                    "I": ["I"]
                    },
            },
        "hemms":
            {
                "PRESENT": {
                    "She": ["She"],
                    "He": ["He"],
                    "We": ["We"],
                    "I": ["I"]
                },
            },
        "is":
            {
                "PRESENT": {
                    "She": ["is"],
                    "He": ["is"],
                    "We": ["are"],
                    "I": ["am"]
                },
            },
        "his":
            {
                "PRESENT": {
                    "She": ["her"],
                    "He": ["his"],
                    "We": ["our"],
                    "I": ["my"]
                },
            },
        "read":
            {
                "PRESENT": {
                    "She": ["reads"],
                    "He": ["reads"],
                    "We": ["read"],
                    "I": ["read"]
                }
            },
        "himmms":
            {
                "PRESENT": {
                    "She": ["her"],
                    "He": ["him"],
                    "We": ["us"],
                    "I": ["me"]
                }
            },
        "himself":
            {
                "PRESENT": {
                    "She": ["herself"],
                    "He": ["himself"],
                    "We": ["ourselves"],
                    "I": ["myslef"]
                }
            },
        "Yuval's":
            {
                "PRESENT": {
                    "She": ["Meirav's", "Inbar's", "her"],
                    "He": ["Michael's", "Amos's", "his"],
                    "We": ["our"],
                    "I": ["my"]
                }
            },
        "Meirav": {
            "PRESENT": {
                "He": [],
                "She": ["Meirav", "Dana"],
                "We": [],
                "I": ["Meirav"]
            }
        },

    }
    assert word in d or word in verbs
    if word in d:
        return d[word][tense][gender]
    return [verbs[word][tense][gender]]
