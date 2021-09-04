from typing import Dict, Tuple, List
from utils import Gender, Tense, Language, capitalize_first_letter
from annotated_word import AnnotatedWord, WordType
import nltk
import replacements_providers
import re
import itertools


class Actor:
    def __init__(self, gender: Gender, index: int, speaker_group: int):
        self.gender = gender
        self.index = index
        self.speaker_group = speaker_group

    def __eq__(self, other):
        return other.gender == self.gender and other.index == self.index and self.speaker_group == other.speaker_group

    def __hash__(self):
        return hash((self.gender, self.index, self.speaker_group))


class ActionMetadata:
    def __init__(self, tense: Tense, verb_group: int):
        self.tense = tense
        self.verb_group = verb_group

    def __eq__(self, other):
        return self.tense == other.tense and self.verb_group == other.verb_group

    def __hash__(self):
        return hash((self.tense, self.verb_group))


class PopulatedPattern:
    def __init__(self, actors: Dict[int, Actor], actions: Dict[int, ActionMetadata]):
        self.actors = actors
        self.actions = actions

    def __eq__(self, other):
        return self.actors == other.actors and self.actions == other.actions

    def __hash__(self):
        return hash((frozenset(self.actors.items()), frozenset(self.actions.items())))


def parse_word_pattern(word_position: int, word_pattern: str) -> AnnotatedWord:
    groups: List[int] = list(re.findall("#_([0-9]+)", word_pattern))
    assert len(groups) <= 1, f"Bad annotation for word: {word_pattern}"
    if not groups:
        # Regular word - not annotated.
        return AnnotatedWord(word_pattern, actual_word=word_pattern, word_position=word_position, speaker_group=1)
    speaker_group = groups[0]
    pattern_parts_no_speaker_group = list(re.split("#_[0-9]+", word_pattern)[1].split("_"))
    action_id = 1
    if pattern_parts_no_speaker_group and pattern_parts_no_speaker_group[0].isnumeric():
        action_id = int(pattern_parts_no_speaker_group[0])
        pattern_parts_no_speaker_group = pattern_parts_no_speaker_group[1:]
    actual_word = pattern_parts_no_speaker_group[-1]
    attrs = pattern_parts_no_speaker_group[:-1]
    pattern_type = WordType.MAGIC
    if WordType.VERB_ANNOTATION in attrs:
        pattern_type = WordType.VERB_ANNOTATION
    prefix = re.split("#_[0-9]+", word_pattern)[0]  # First characters before the #_NUMBER annotation.
    if "נ" in attrs or "F" in attrs:
        gender = Gender.SHE
    elif "ז" in attrs or "M" in attrs:
        gender = Gender.HE
    else:
        gender = None

    tense = None
    if "עבר" in attrs or "past" in attrs:
        tense = Tense.PAST
    if "הווה" in attrs or "present" in attrs:
        tense = Tense.PRESENT
    if "עתיד" in attrs or "future" in attrs:
        tense = Tense.FUTURE

    return AnnotatedWord(word_pattern, actual_word=actual_word, word_position=word_position,
                         speaker_group=int(speaker_group), prefix=prefix, word_type=pattern_type,
                         gender=gender, tense=tense, action_id=action_id)


def tokenize(pattern: str) -> List[str]:
    # Allow letters '#' '_' numbers and Hebrew diacritics to be in the same word.
    # Hebrew diacritics range: "\u0590-\u05CF"
    return nltk.RegexpTokenizer(rf"[\w\#\u0590-\u05CF\+']+|[^\w\s]+").tokenize(pattern)


def get_replacement(word: AnnotatedWord, actor: Actor, action_meta: ActionMetadata, lang: Language) -> str:
    gender_replacements = replacements_providers.get_replacements(word, actor.gender, action_meta.tense, lang)
    if len(gender_replacements) > 1 and actor.index > len(gender_replacements) - 1:
        return None
    return gender_replacements[actor.index] if len(gender_replacements) > 1 else gender_replacements[0]


def _pop_sentence(populated_pattern: PopulatedPattern, words: [AnnotatedWord], lang: Language):
    word: AnnotatedWord
    populated_sentence = []
    for word in words:
        if word.type != WordType.REGULAR:
            actor = populated_pattern.actors[word.speaker_group]
            action_meta = populated_pattern.actions[word.action_id]
            word.new_word = get_replacement(word, actor, action_meta, lang)
            if word.new_word is None:
                return
        else:
            word.new_word = word.actual_word
        populated_sentence.append(word)
    s = " ".join([(word.prefix + word.new_word) for word in populated_sentence])
    s = s.replace(" .", ".").replace(" ,", ",").replace(" !", "!").replace(" ?", "?")
    s = capitalize_first_letter(s)
    return s


def get_all_actors(speaker_group):
    actions = []
    for gender in [Gender.SHE, Gender.HE, Gender.I_F, Gender.I_M]:
        for index in range(4):
            actions.append(Actor(gender, index, speaker_group))
    return actions


def get_all_actions(verb_group):
    a1 = ActionMetadata(Tense.PAST, verb_group)
    a2 = ActionMetadata(Tense.PRESENT, verb_group)
    return [a1, a2]


def populate_pattern(sent: str, lang: Language,
                     static_replacements_dict_or_none: Dict[str, str] = None,
                     tenses_white_list: List[Tense] = None) -> Dict[PopulatedPattern, str]:
    pattern_words: List[str] = tokenize(sent)
    parsed_words: List[AnnotatedWord] = [parse_word_pattern(pos, pattern) for pos, pattern in enumerate(
        pattern_words)]
    speaker_groups: List[int] = list(sorted({word.speaker_group for word in parsed_words}))
    actions: List[int] = list(sorted({word.action_id for word in parsed_words if word.action_id is not None}))
    actions = actions if actions else [1]
    actors = [get_all_actors(sg) for sg in speaker_groups]
    all_actions = [(get_all_actions(ac)) for ac in actions]
    out = {}
    for actors_assignment in itertools.product(*actors):
        for actions_assignment in itertools.product(*all_actions):
            p = PopulatedPattern({actor.speaker_group: actor for actor in actors_assignment},
                                 {action.verb_group: action for action in actions_assignment})
            s = _pop_sentence(p, parsed_words, lang)
            if s:
                out[p] = s
    return out


if __name__ == "__main__":
    out1 = populate_pattern("#_1_someone #_1_missed #_2_someone+obj", Language.ENGLISH)
    out2 = populate_pattern("#_2_מישהו #_2_חסר #_1_למישהו", Language.HEBREW)
