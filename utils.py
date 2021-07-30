import nltk


def capitalize_first_letter(st: str):
    if not st:
        return st
    return st[0].upper() + st[1:]


def compute_bleu(ref,  translation):
    return nltk.translate.bleu_score.sentence_bleu([ref], translation)
