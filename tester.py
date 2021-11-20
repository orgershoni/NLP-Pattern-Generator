import he_en_translator
from patterns_populator_ng import populate_pattern
from utils import compute_bleu
from typing import List, Tuple
import pandas as pd
import argparse
import sys
from utils import Language
import tqdm
import google_translate


def generate_sentences(sentence_pairs: List[Tuple[str, str]]):

    heb_text_to_translate = []
    english_reference = []
    hebrew_src_sentences = []
    print("Starting to populate patterns")
    for i, pair in tqdm.tqdm(enumerate(sentence_pairs)):

        hebrew_sentences, english_sentences = generate_sentences_for_single_origin(pair)
        heb_text_to_translate.extend(hebrew_sentences)
        english_reference.extend(english_sentences)
        hebrew_src_sentences.extend(hebrew_sentences)

    return heb_text_to_translate, english_reference, hebrew_src_sentences


def generate_sentences_for_single_origin(sentence_pair: Tuple[str, str]):
    # The generated hebrew and english sentences are parallel (in term of order).
    hebrew_sentences = populate_pattern(sentence_pair[0], Language.HEBREW)
    english_sentences = populate_pattern(sentence_pair[1], Language.ENGLISH)
    assert len(hebrew_sentences) == len(english_sentences), f"pattern: {sentence_pair[0]}\n{sentence_pair[1]}\n" \
                                                            f"{hebrew_sentences}\n{english_sentences}"
    # TODO explain why there are duplicates.
    unique_pairs = set()
    for meta, sentence in hebrew_sentences.items():
        unique_pairs.add((sentence, english_sentences[meta]))
    hebrew_sentences = [pair[0] for pair in unique_pairs]
    english_sentences = [pair[1] for pair in unique_pairs]

    return hebrew_sentences, english_sentences


def main(sentence_pairs: List[Tuple[str, str]], output_path: str):

    heb_sentences, english_reference, hebrew_src_sentences = generate_sentences(sentence_pairs)
    print(f"Translating src sentences. Num lines: {len(heb_sentences)}")
    translated_sentences = google_translate.Translator().translate(heb_sentences, Language.HEBREW, Language.ENGLISH)
    bleu_scores = []
    print("Computing bleu")
    for translated_sent, sent_ref in zip(translated_sentences, english_reference):
        bleu_scores.append(compute_bleu(sent_ref, translated_sent))
    out_df = pd.DataFrame.from_dict({"Hebrew src": hebrew_src_sentences,
                                     "English Reference": english_reference,
                                     "English Translation": translated_sentences,
                                     "Score": bleu_scores})
    out_df.to_csv(output_path, encoding="utf-8")


if __name__ == "__main__":
    tup = tuple("#_1_אין #_1_חפץ+פיזי בכל המדינה,there are no #_1_physical+object in the entire country".split(','))
    generate_sentences_for_single_origin(tup)
