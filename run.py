import he_en_translator
from patterns_generator import populate_pattern
from utils import compute_bleu
from typing import List, Tuple
import pandas as pd
import argparse
import sys


def main(sentence_paris: List[Tuple[str, str]]):
    # x = "#_1_אין #_1_למישהו כוח היום ללמוד"
    # y = "#_1_someone #_1_didn't feel like studying today"
    text_to_translate = ""
    english_reference = []
    hebrew_src_sentences = []
    for pair in sentence_paris:
        hebrew_sentences = populate_pattern(pair[0], "hebrew", None)
        english_sentences = populate_pattern(pair[1], "english", None)
        assert len(hebrew_sentences) == len(english_sentences)
        text_to_translate += "\n".join(hebrew_sentences) + "\n"
        english_reference.extend(english_sentences)
        hebrew_src_sentences.extend(hebrew_sentences)
    translated_sentences = he_en_translator.translate(text_to_translate)
    bleu_scores = []
    for translated_sent, sent_ref in zip(translated_sentences, english_reference):
        bleu_scores.append(compute_bleu(sent_ref, translated_sent))
    df = pd.DataFrame.from_dict({"HebrewSrc": hebrew_src_sentences, "EnglishRef": english_reference, "EnglishTrns":
        translated_sentences, "score": bleu_scores})
    df.to_csv("op.csv", encoding="utf-8")


def get_input_pattern():
    hebrew_sent = input("Enter the Hebrew pattern\n")
    english_sent = input("Enter the English pattern\n")
    return [(hebrew_sent, english_sent)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Takes parallel input patterns in src and dst languages, '
                                                 'populates the patterns, translates the src language and'
                                                 ' compares to the dst populated patterns using bleu score.')
    parser.add_argument("patterns_file", type=str, help="file of format TODO of patterns.", default="")
    parser.add_argument("inline_pattern", type=bool, default=False)
    args = parser.parse_args(sys.argv)
    patterns = []
    if args.inline_pattern:
        patterns = get_input_pattern()
    elif args.patterns_file:
        patterns = []  # Todo read from file format
    else:
        print("Error: either `patterns_file` or `inline_pattern` should be provided")
        exit(1)
    main(patterns)
