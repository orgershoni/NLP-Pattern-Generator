from enum import Enum
from utils import Gender, Tense


class WordType(Enum):
    REGULAR = "REGULAR"
    MAGIC = "Magic"
    VERB_ANNOTATION = "פועל"


class AnnotatedWord:
    def __init__(self, pattern: str, actual_word: str, word_position: int, speaker_group: int = 0,
                 word_type: WordType = WordType.REGULAR,
                 prefix="", gender: Gender = None, tense: Tense = None, action_id=None):
        self.pattern: str = pattern
        self.speaker_group: int = speaker_group
        self.actual_word: str = actual_word
        self.type: WordType = word_type
        self.word_position: int = word_position
        self.prefix: str = prefix
        self.gender = gender
        self.tense = tense
        self.action_id = action_id

    def __str__(self):
        return f"content: {self.pattern}\ngroup: {self.speaker_group}\nrole:" \
               f" {self.actual_word}\ntype: {self.type}\n"

