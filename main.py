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


def generate_sentences(sentence_pairs: List[Tuple[str, str]], src: Language, dest: Language):

    src_text_to_translate = []
    dest_reference = []
    src_orig_sentences = []
    print("Starting to populate patterns")
    for i, pair in tqdm.tqdm(enumerate(sentence_pairs)):
        # The generated hebrew and english sentences are parallel (in term of order).
        src_sentences = populate_pattern(pair[0], src)
        dest_sentences = populate_pattern(pair[1], dest)
        assert len(src_sentences) == len(dest_sentences), f"pattern: {i+1}\n {pair[0]}\n{pair[1]}\n" \
                                                                f"{src_sentences}\n{dest_sentences}"
        # TODO explain why there are duplicates.
        unique_pairs = set()
        for meta, sentence in src_sentences.items():
            unique_pairs.add((sentence, dest_sentences[meta]))
        src_sentences = [pair[0] for pair in unique_pairs]
        dest_sentences = [pair[1] for pair in unique_pairs]
        src_text_to_translate.extend(src_sentences)
        dest_reference.extend(dest_sentences)
        src_orig_sentences.extend(src_sentences)

    return src_text_to_translate, dest_reference, src_orig_sentences


def main(sentence_pairs: List[Tuple[str, str]], src: Language, dest: Language, output_path: str):

    src_sentences, dest_reference, src_orig_sentences = generate_sentences(sentence_pairs, src, dest)
    print(f"Translating src sentences. Num lines: {len(src_sentences)}")
    translated_sentences = google_translate.Translator().translate(src_sentences, src, dest)
    bleu_scores = []
    print("Computing bleu")
    for translated_sent, sent_ref in zip(translated_sentences, dest_reference):
        bleu_scores.append(compute_bleu(sent_ref, translated_sent))
    out_df = pd.DataFrame.from_dict({"Hebrew src": src_orig_sentences,
                                     "English Reference": dest_reference,
                                     "English Translation": translated_sentences,
                                     "Score": bleu_scores})
    out_df.to_csv(output_path, encoding="utf-8")


def parse_languages(src_language:str, dest_language:str) -> Tuple[Language, Language]:

    supported_langs = [e.name for e in Language]
    if src_language not in supported_langs:
        raise KeyError(f"{src_language} is not supported")
    if dest_language not in supported_langs:
        raise KeyError(f"{dest_language} is not supported")

    return Language[src_language], Language[dest_language]



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Takes parallel input patterns in src and dst languages, '
                                                 'populates the patterns, translates the src language and'
                                                 ' compares to the dst populated patterns using bleu score.')
    parser.add_argument("patterns_file", type=str, help="file of format TODO of patterns.", default="")
    parser.add_argument("src_language", type=str, help=f"supported languages: {[e.name for e in Language]}", default="")
    parser.add_argument("dest_language", type=str, help=f"supported languages: {[e.name for e in Language]}", default="")
    parser.add_argument("-o", "--output_path", help="output path", default="scores.csv")
    parser.add_argument("--pattern_indices", action='append', type=int, help="index of pattern in pattern file, "
                                                                             "0-based index.")
    args = parser.parse_args(sys.argv[1:])
    src, dest = parse_languages(args.src_language, args.dest_language)
    df = pd.read_csv(args.patterns_file, encoding="utf-8", header=None)
    patterns = list(df.itertuples(index=False, name=None))
    if args.pattern_indices:
        patterns = [patterns[i] for i in args.pattern_indices]
    print(f"Num patterns: {len(patterns)}")
    main(patterns, src, dest, args.output_path)
