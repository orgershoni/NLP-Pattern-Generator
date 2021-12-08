from typing import List, Tuple
import pandas as pd
import argparse
import sys


def _populate_patterns(abstract_patterns: List[Tuple[str, str]],
                       verbs_to_populate: List[Tuple[str, str]]):
    new_patterns = []
    for hebrew_verb, english_verb in verbs_to_populate:
        for hebrew_pattern, english_pattern in abstract_patterns:
            new_patterns.append((hebrew_pattern.replace("קסם", hebrew_verb),
                                 english_pattern.replace("magic", english_verb)))
    return new_patterns


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("in_path", type=str, help="Input file.", default="")
    parser.add_argument("out_path", help="output path", default="")
    args = parser.parse_args(sys.argv[1:])
    df = pd.read_csv(args.in_path, encoding="utf-8", header=None)
    rows = [row[1] for row in df.iterrows()]
    patterns: List[Tuple[str, str]] = []
    word_replacements: List[Tuple[str, str]] = []
    # First rows are the patterns, which should contain `#`, the rest should not.
    i = 0
    while i < len(rows) and "#" in rows[i][0]:
        patterns.append((rows[i][0], rows[i][1]))
        i += 1
    while i < len(rows):
        assert "#" not in rows[i][0]
        word_replacements.append((rows[i][0], rows[i][1]))
        i += 1
    out_df = pd.DataFrame.from_records(_populate_patterns(patterns, word_replacements))
    out_df.to_csv(args.out_path, header=False, index=False)
