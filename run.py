import he_en_translator
from patterns_generator import populate_pattern
from utils import compute_bleu
from typing import List, Tuple
import pandas as pd


def main():
    # Read input sentences
    x = "#_1_אין #_1_למישהו כוח היום ללמוד"
    y = "#_1_someone #_1_didn't feel like studying today"
    sentence_paris: List[Tuple[str, str]] = [(x, y)]
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
    print(df)


if __name__ == "__main__":
    main()
