from utils import Language, chunks
import translators.google_translate as google_translate

def translate(sentences, src: Language, dest : Language):

    splitted_sentences = chunks(sentences, google_translate.MAX_QUATA)
    translated = []
    for src_sentences in splitted_sentences:
        translated_sentences = google_translate.Translator().translate(src_sentences, src, dest)
        translated.extend(translated_sentences)

    return translated