import he_en_translator
from patterns_generator import populate_pattern
from utils import compute_bleu
from typing import List, Tuple
import pandas as pd
import argparse
import sys
from utils import Language


def main(sentence_pairs: List[Tuple[str, str]], output_path: str):
    text_to_translate = ""
    english_reference = []
    hebrew_src_sentences = []
    print("Starting to populate patterns")
    for pair in sentence_pairs:
        # The generated hebrew and english sentences are parallel (in term of order).
        hebrew_sentences = populate_pattern(pair[0], Language.HEBREW, None)
        english_sentences = populate_pattern(pair[1], Language.ENGLISH, None)
        assert len(hebrew_sentences) == len(english_sentences)
        # TODO explain why there are duplicates.
        unique_pairs = list(dict.fromkeys(zip(hebrew_sentences, english_sentences)))
        hebrew_sentences = [pair[0] for pair in unique_pairs]
        english_sentences = [pair[1] for pair in unique_pairs]
        text_to_translate += "\n".join(hebrew_sentences) + "\n"
        english_reference.extend(english_sentences)
        hebrew_src_sentences.extend(hebrew_sentences)
    print("Translating src sentences")
    translated_sentences = he_en_translator.translate(text_to_translate)
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
    args = parser.parse_args(sys.argv[1:])
    df = pd.read_csv(args.patterns_file, encoding="utf-8", header=None)
    patterns = list(df.itertuples(index=False, name=None))
    print(f"Num patterns: {len(patterns)}")
    main(patterns, args.output_path)