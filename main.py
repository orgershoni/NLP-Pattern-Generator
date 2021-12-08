from utils import compute_bleu
from typing import List, Tuple
import pandas as pd
import argparse
import sys
from utils import Language
from translators.translate import translate
from populate_patterns.main import populate
from estimation.bleu import bleu



def parse_args(parser):
    parser.add_argument("patterns_file", type=str, help="file of format TODO of patterns.", default="")
    parser.add_argument("src_language", type=str, choices=[e.name for e in Language], default="")
    parser.add_argument("dest_language", type=str, choices=[e.name for e in Language], default="")
    parser.add_argument("-o", "--output_path", help="output path", default="scores.csv")
    parser.add_argument("--pattern_indices", action='append', type=int, help="index of pattern in pattern file, "
                                                                             "0-based index.")
    parser.add_argument("-rcd", "--remove-disambg-cache", help="remove disambiguity cache", action='store_true', default=False)

    args = parser.parse_args(sys.argv[1:])

    src = Language[args.src_language]
    dest = Language[args.dest_language]
    
    df = pd.read_csv(args.patterns_file, encoding="utf-8", header=None)
    patterns = list(df.itertuples(index=False, name=None))
    if args.pattern_indices:
        patterns = [patterns[i] for i in args.pattern_indices]
    print(f"Num patterns: {len(patterns)}")

    return patterns, src, dest, args.output_path, args.remove_disambg_cache

def main(sentence_pairs: List[Tuple[str, str]], src: Language, dest: Language, output_path: str, remove_disambiguity_cache=False):

    print(f"Generating setences out of {len(sentence_pairs)} patterns")
    src_sentences, dest_reference, src_orig_sentences = populate(sentence_pairs, src, dest, remove_disambiguity_cache)

    print(f"Translating src sentences. Num lines: {len(src_sentences)}")
    translated_sentences = translate(src_sentences, src, dest)
    
    print("Computing bleu")
    bleu_scores = bleu(translated_sentences, dest_reference)

    # Save to csv
    pd.DataFrame.from_dict({"Hebrew src": src_orig_sentences,
                            "English Reference": dest_reference,
                            "English Translation": translated_sentences,
                            "Bleu Score": bleu_scores,
                            }) \
                            .to_csv(output_path, encoding="utf-8")


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

    main(*parse_args(parser))
