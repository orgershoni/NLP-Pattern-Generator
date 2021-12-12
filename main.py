from utils import GeneratedSentence, lower_all
from typing import List, Tuple
import pandas as pd
import argparse
import sys
from utils import Language
from translators.translate import translate
from populate_patterns.main import populate
from estimation.bleu import bleu
from estimation.consistency import patterns_levenshtein
from cache_manager.manager import CacheOptions, g_cache_manager



def parse_args(parser):
    import os
    parser.add_argument("patterns_file", type=str, help="file of format TODO of patterns.", default="")
    parser.add_argument("src_language", type=str, choices=[e.name for e in Language], default="")
    parser.add_argument("dest_language", type=str, choices=[e.name for e in Language], default="")
    parser.add_argument("-o", "--output_path", help="output path", default="scores.csv")
    parser.add_argument("--pattern_indices", action='append', type=int, help="index of pattern in pattern file, "
                                                                             "0-based index.")
    parser.add_argument("-rcd", "--remove-disambg-cache", help="remove disambiguity cache", action='store_true', default=False)
    parser.add_argument("-gta", "--google-translate-auth", help="Path to JSON file contains Google Translate credentials", default="")


    args = parser.parse_args(sys.argv[1:])

    src = Language[args.src_language]
    dest = Language[args.dest_language]
    
    if args.google_translate_auth:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.google_translate_auth
        g_cache_manager.cache_google_auth(args.google_translate_auth)
    else:
        try:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = g_cache_manager.load_google_auth()
        except ValueError:
            pass
        
    df = pd.read_csv(args.patterns_file, encoding="utf-8", header=None)
    patterns = list(df.itertuples(index=False, name=None))
    if args.pattern_indices:
        patterns = [patterns[i] for i in args.pattern_indices]
    print(f"Num patterns: {len(patterns)}")

    return patterns, src, dest, args.output_path, args.remove_disambg_cache

def get_sentences(generated_sentences : List[GeneratedSentence]):

    return [gen_sentence.sentence for gen_sentence in generated_sentences]

def load_script_cache() -> CacheOptions:

    print("Loading cache...")
    try:
        src, dest = g_cache_manager.load_generated_sentences()
    except ValueError as e:
        src = None
    
    if src : 
        try:
            translated = g_cache_manager.load_translated_sentences()
            print("Loaded cached generated sentences and translated sentences")
            return src, dest, src, translated
        except ValueError as e:
            print("Loaded cached generated sentences")
            print(f"Error was : {str(e)}")
            return src, dest, src, None
    else:
        print("No cache found")
        return None, None, None, None

def main(sentence_pairs: List[Tuple[str, str]], src: Language, dest: Language, output_path: str, remove_disambiguity_cache=False):

    src_sentences, dest_reference, src_orig_sentences, translated_sentences = load_script_cache()

    if not src_sentences:
        print(f"Generating setences out of {len(sentence_pairs)} patterns")
        src_sentences, dest_reference, src_orig_sentences = populate(sentence_pairs, src, dest, remove_disambiguity_cache)
        g_cache_manager.cache_generated_sentences(src_sentences, dest_reference)

    if not translated_sentences:
        print(f"Translating src sentences. Num lines: {len(src_sentences)}")
        translated_sentences = lower_all(translate(src_sentences, src, dest))
        g_cache_manager.cache_translated_sentences(translated_sentences)
    
    print("Computing bleu")
    bleu_scores = bleu(translated_sentences, get_sentences(dest_reference))

    # TODO : we don't care about reference here, we measure consistency between sentences of the same pattern
    patterns_levenshtein(translated_sentences, dest_reference)
    # Save to csv
    pd.DataFrame.from_dict({f"{src.name} src": src_orig_sentences,
                            f"{dest.name} Reference": get_sentences(dest_reference),
                            f"{dest.name} Translation": translated_sentences,
                            "Bleu Score": bleu_scores,
                            }) \
                            .to_csv(output_path, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Takes parallel input patterns in src and dst languages, '
                                                 'populates the patterns, translates the src language and'
                                                 ' compares to the dst populated patterns using bleu score.')

    main(*parse_args(parser))
