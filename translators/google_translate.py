from google.cloud import translate_v2
from utils import Language
from typing import List
from google.auth.exceptions import DefaultCredentialsError


_language_code_639 = {
    Language.ENGLISH: "en",
    Language.HEBREW: "he",
    Language.FRENCH: "fr",
    Language.ARABIC: "ar",
}

MAX_QUATA = 100
GOOGLE_AUTH_ERROR = "The translation system being tested is Google Translate," \
                    "please provide credentials to Google Cloud to continue." \
                    " Set GOOGLE_APPLICATION_CREDENTIALS enviroment variable with a path to .json credentials path" \
                    "before running this script" 

try:
    translator = translate_v2.Client()
    print("initialized g translate succesfully")
except DefaultCredentialsError:
    print(GOOGLE_AUTH_ERROR)
    exit(1)

class Translator:

    def translate(self, sentences: List[str], src_lang: Language, dst_lang: Language):
        results = translator.translate(sentences, target_language=_language_code_639[dst_lang],
                                                   source_language=_language_code_639[src_lang],
                                                   format_="text")
        return [result["translatedText"] for result in results]


if __name__ == "__main__":
    print(Translator().translate(["I love her so much"], Language.ENGLISH, Language.FRENCH))