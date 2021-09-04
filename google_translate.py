from google.cloud import translate_v2
from utils import Language
from typing import List
import os


_language_code_639 = {
    Language.ENGLISH: "en",
    Language.HEBREW: "he",
    Language.FRENCH: "fr",
}


class Translator:

    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\omryg\Downloads\prefab-research-113417-7d917e3533d8" \
                                                     r".json"
        self._translate_client = translate_v2.Client()

    def translate(self, sentences: List[str], src_lang: Language, dst_lang: Language):
        results = self._translate_client.translate(sentences, target_language=_language_code_639[dst_lang],
                                                   source_language=_language_code_639[src_lang],
                                                   format_="text")
        return [result["translatedText"] for result in results]


if __name__ == "__main__":
    print(Translator().translate(["I love her so much"], Language.ENGLISH, Language.FRENCH))