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
        # The generated hebrew and english sentences are parallel (in term of order).
        hebrew_sentences = populate_pattern(pair[0], Language.HEBREW)
        english_sentences = populate_pattern(pair[1], Language.ENGLISH)
        assert len(hebrew_sentences) == len(english_sentences), f"pattern: {i+1}\n {pair[0]}\n{pair[1]}\n" \
                                                                f"{hebrew_sentences}\n{english_sentences}"
        # TODO explain why there are duplicates.
        unique_pairs = set()
        for meta, sentence in hebrew_sentences.items():
            unique_pairs.add((sentence, english_sentences[meta]))
        hebrew_sentences = [pair[0] for pair in unique_pairs]
        english_sentences = [pair[1] for pair in unique_pairs]
        heb_text_to_translate.extend(hebrew_sentences)
        english_reference.extend(english_sentences)
        hebrew_src_sentences.extend(hebrew_sentences)

    return heb_text_to_translate, english_reference, hebrew_src_sentences


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
    parser = argparse.ArgumentParser(description='Takes parallel input patterns in src and dst languages, '
                                                 'populates the patterns, translates the src language and'
                                                 ' compares to the dst populated patterns using bleu score.')
    parser.add_argument("patterns_file", type=str, help="file of format TODO of patterns.", default="")
    parser.add_argument("-o", "--output_path", help="output path", default="scores.csv")
    parser.add_argument("--pattern_indices", action='append', type=int, help="index of pattern in pattern file, "
                                                                             "0-based index.")
    args = parser.parse_args(sys.argv[1:])
    df = pd.read_csv(args.patterns_file, encoding="utf-8", header=None)
    patterns = list(df.itertuples(index=False, name=None))
    if args.pattern_indices:
        patterns = [patterns[i] for i in args.pattern_indices]
    print(f"Num patterns: {len(patterns)}")
    main(patterns, args.output_path)
