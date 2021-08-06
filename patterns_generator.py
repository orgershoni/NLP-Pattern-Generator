from typing import List, Tuple, Dict
from annotated_word import AnnotatedWord, WordType
import itertools
import re
import utils
from replacements_providers import get_replacements
import nltk
from utils import Language, Gender, Tense


def parse_word_pattern(word_position: int, word_pattern: str) -> AnnotatedWord:
    groups: List[int] = list(re.findall("#_([0-9]+)", word_pattern))
    assert len(groups) <= 1, f"Bad annotation for word: {word_pattern}"
    if not groups:
        # Regular word - not annotated.
        return AnnotatedWord(word_pattern, actual_word=word_pattern, word_position=word_position)
    speaker_group = groups[0]
    pattern_parts_no_speaker_group = list(re.split("#_[0-9]+", word_pattern)[1].split("_"))
    actual_word = pattern_parts_no_speaker_group[-1]
    attrs = pattern_parts_no_speaker_group[:-1]
    pattern_type = WordType.MAGIC
    if WordType.VERB_ANNOTATION in attrs:
        pattern_type = WordType.VERB_ANNOTATION
    prefix = re.split("#_[0-9]+", word_pattern)[0]  # First characters before the #_NUMBER annotation.
    return AnnotatedWord(word_pattern, actual_word=actual_word, word_position=word_position, speaker_group=int(speaker_group),
                         prefix=prefix, word_type=pattern_type)


def tokenize(pattern: str) -> List[str]:
    return nltk.RegexpTokenizer(r"[\w\#']+|[^\w\s]+").tokenize(pattern)


def get_all_combinations_for_single_speaker_group(group_words: List[AnnotatedWord], gender: Gender, tense: Tense,
                                                  lang: Language)\
        -> List[List[Tuple[str, int]]]:
    per_word_replacements: List[List[Tuple[str, int]]] = []
    for word in group_words:
        word_replacements: List[str] = get_replacements(word, gender, tense, lang)
        word_replacements_with_index = [(replacement, word.word_position) for replacement in word_replacements]
        per_word_replacements.append(word_replacements_with_index)
    return [list(combination)
            for combination in itertools.product(*per_word_replacements)]


def populate_pattern(sent: str, lang: Language,
                     static_replacements_dict_or_none: Dict[str, str] = None):

    pattern_words: List[str] = tokenize(sent)
    parsed_words: List[AnnotatedWord] = [parse_word_pattern(pos, pattern) for pos, pattern in enumerate(
        pattern_words)]

    # E.g. #_1_someone called #_2_someone => speaker_groups:= [1, 2]
    speaker_groups: List[int] = list(sorted({word.speaker_group for word in parsed_words}))
    per_group_combinations: List[List[List[Tuple[str, int]]]] = []
    for speaker in speaker_groups:
        speaker_words = [word for word in parsed_words if word.speaker_group == speaker]
        group_combs = []
        for gender, tense in [(Gender.II, Tense.PAST), (Gender.SHE, Tense.PAST), (Gender.SHE, Tense.PRESENT),
                              (Gender.HE, Tense.PRESENT), (Gender.WE, Tense.PRESENT), (Gender.II, Tense.PRESENT)]:
            group_combs.extend(get_all_combinations_for_single_speaker_group(speaker_words, gender, tense, lang))
        per_group_combinations.append(group_combs)
    all_sentences = []
    for single_replacement_per_group in itertools.product(*per_group_combinations):
        sent = list(itertools.chain(*list(single_replacement_per_group)))
        sent = [_y[0] for _y in sorted(sent, key=lambda _x: _x[1])]
        all_sentences.append(tuple(sent))

    all_sentences_text = []
    for sent in all_sentences:
        all_sentences_text.append(" ".join(
            [parsed_words[i].prefix + word for i, word in enumerate(sent)])
        )
    sentences = [sent.replace(" .", ".").replace(" ,", ",").replace(" !", "!").replace(" ?", "?")
                 for sent in all_sentences_text]
    if static_replacements_dict_or_none:
        for word, replacement in static_replacements_dict_or_none.items():
            sentences = [sent.replace(word, replacement) for sent in sentences]
    return [*map(utils.capitalize_first_letter, sentences)]


if __name__ == "__main__":
    src_lang_input = input("Enter a pattern in Hebrew\n")
    dst_lang_input = input("Enter a pattern in English\n")
    print("Populating patterns")
    __black_list = []
    src_populated_patterns = populate_pattern(src_lang_input, Language.HEBREW)
    dst_populated_patterns = populate_pattern(dst_lang_input, Language.ENGLISH)
    assert len(src_populated_patterns) == len(dst_populated_patterns), f"{set(src_populated_patterns)}\
    n{set(dst_populated_patterns)}"
    __sentences = set(zip(src_populated_patterns, dst_populated_patterns))
    for __sent1, __sent2 in __sentences:
        print(f"{__sent1}\n{__sent2}\n\n")
