from typing import List, Tuple
from annotated_word import Word
import itertools
import re
import utils
from replacements_providers import get_replacements
import nltk


POAL = "פועל"


def annotate_word(word: str, word_position) -> Word:
    groups: List[int] = list(re.findall("#_([0-9]+)", word))
    assert len(groups) <= 1, f"Bad annotation for word: {word}"
    if not groups:
        return Word(word, word_position=word_position)
    group = groups[0]
    content = list(re.split("#_[0-9]+", word)[1].split("_"))
    prefix = re.split("#_[0-9]+", word)[0]
    w = Word(word, int(group), role=content[-1], word_position=word_position, prefix=prefix)
    attrs = [attr for attr in content[:-1] if attr]
    if POAL in attrs:
        w.type = POAL
    else:
        w.type = "Magic"
    return w


def tokenize(sent: str) -> List[str]:
    words = nltk.WordPunctTokenizer().tokenize(sent.replace("#", "אבגדה").replace("'", "XXX"))
    return [word.replace("אבגדה", "#").replace("XXX", "'") for word in words]


def get_all_combinations_for_single_speaker_group(group_words: List[Word], gender, tense, lang)\
        -> List[List[Tuple[str, int]]]:
    per_word_replacements: List[List[Tuple[str, int]]] = []
    for word in group_words:
        word_replacements: List[str] = get_replacements(word, gender, tense, lang)
        word_replacements_with_index = [(replacement, word.word_position) for replacement in word_replacements]
        per_word_replacements.append(word_replacements_with_index)
    return [list(combination)
            for combination in itertools.product(*per_word_replacements)]


def populate_pattern(sent: str, lang, static_replacements_dict):

    words = tokenize(sent)
    annotated_words: List[Word] = [annotate_word(word, i) for i, word in enumerate(words)]

    speaker_groups = list(sorted({word.group for word in annotated_words}))
    per_group_combinations: List[List[List[Tuple[str, int]]]] = []
    for group in speaker_groups:
        group_words = [word for word in annotated_words if word.group == group]
        group_combs = []
        for gender, tense in [("I", "PAST"), ("She", "PAST"), ("She", "PRESENT"),
                              ("He", "PRESENT"), ("We", "PRESENT"), ("I", "PRESENT")]:
            group_combs.extend(get_all_combinations_for_single_speaker_group(group_words, gender, tense, lang))
        per_group_combinations.append(group_combs)
    all_sentences = []
    for single_replacement_per_group in itertools.product(*per_group_combinations):
        sent = list(itertools.chain(*list(single_replacement_per_group)))
        sent = [_y[0] for _y in sorted(sent, key=lambda _x: _x[1])]
        all_sentences.append(tuple(sent))

    all_sentences_text = []
    for sent in all_sentences:
        all_sentences_text.append(" ".join(
            [annotated_words[i].prefix + word for i, word in enumerate(sent)])
        )
    sentences = [sent.replace(" .", ".").replace(" ,", ",").replace(" !", "!").replace(" ?", "?")
                 for sent in all_sentences_text]
    if static_replacements_dict:
        sentences = [sent.replace(static_replacements_dict[0], static_replacements_dict[1]) for sent in sentences]
    return [utils.capitalize_first_letter(sent) for sent in sentences]


if __name__ == "__main__":
    s = "#_1_היא #_1_הלכה לבית #_2_שלה"
    s = "#_1_היא לא #_1_אמרה #_2_לה"
    s = "אין #_1_לה מצב רוח"
    s = "#_1_היא #_1_הקריאה ל #_1_בנה סיפור"
    s = "קוראים #_1_לה למטה"
    s = "קוראים #_1_לה לאכול"
    s = "ההורים ש_ #_1_לה קוראים #_2_לה סיפור לפני השינה"
    s = "#_1_פועל_הקריאה מ_ #_1_צלחתה של #_1_יובל"
    s = "#_1_הקריאה #_2_לה כבשה"
    s = "הטלפון הלך #_1_לה לאיבוד"
    s = "#_1_היא #_1_הקריאה ב_ #_2_יובל"
    s = "מגיע #_1_לה כי #_1_היא-ממש #_1_הקריאה לא יפה"
    s = "#_1_היא #_1_הקריאה בזכות כוח הרצון #_1_שלה-ממש"
    s = "לא מתחשק #_1_לה לאכול"
    s = "לא מתחשק ל_ #_1_עמוס #_2_בנה של #_2_יובל"
    s = "לא אכפת #_1_לו אם #_2_הוא #_2_רצה לאכול איתי"
    #verbs_table = create_verbs_table(r"C:\Users\omryg\Downloads\InflectedVerbsExtended.csv")

    #s = "#_1_יובל #_1_הקריאה ל #_1_בנה סיפור"
    #s = "קוראים #_1_לה #_1_יובל"
    s = "#_1_הוא #_1_הלך ל_ #_2_מקום"
    s = "אין #_1_לו מצב רוח"
    s = "#_1_הוא #_1_קרא #_2_לו סיפור"
    s = "ההורים #_1_שלו קוראים #_2_לו-ממש סיפור לפני השינה"
    s = "#_1_אכל #_2_לו-ממש מהצלחת"
    s = "מגרד #_2_לו בגב"
    s = "הראש #_1_שלו מגרש"
    x = "מכנים אות#_1_ו #_1_יובל"
    y = "#_1_he #_1_was called #_1_Yuval"
    s = "תעשה ל#_1_עמוס בנו של #_2_עמוס בבקשה #_1_עמוס"
    s = "#_1_פועל_גרד בראש"
    s = "תעשה ל#_1_מירב , בתו של #_2_עמוס , מקום"
    from pprint import pprint
    #x = "תעשה ל#_1_מירב, בתו של #_2_עמוס, מקום"
    #y = "make room to #_1_Meirav, #_2_Amos 's daughter"
    # x = "#_1_ציר לי כבשה!"
    # x = "#_1_פזם לעצמ#_1_ו שיר"
    # x = "#_1_הכין #_1_לוממש חביתה"
    # x = "הטלפון הלך #_2_לו לאיבוד"
    x = "#_1_מישהו #_1_נטה להפגע בקלות"
    y = "#_1_someone #_1_tended to get hurt easily"
    # x = "#_1_מישהו #_1_הכין ב#_2_יובל"
    # y = "#_1_someone believed in #_2_Yuval"
    # #x = "#_1_מישהו #_1_הכין בחיים בזכות הרצון #_1_שלו"
    #y = "#_1_someone succeeded in life thanks to #_1_his will power"
    #x = "#_1_למישהו לא משנה מה #_2_עמוס, חתול#_1_ו הקטן, יגיד"
    #y = "#_1_someone #_1_didn't care about what #_2_Amos, #_1_his little cat, will say"
    #x = "לא #_1_האמין לאף אחד"
    #x = "#_1_מישהו לא #_1_הכין דבר כזה מימי#_1_ו"
    #y = "#_1_someone #_1_didn't see such a thing in #_1_his life"
    #x = "#_1_הוא #_1_הלך לבית הספר"

    #x = "#_1_מישהו #_1_הכין ל#_2_יובל סיפור"
    #y = "#_1_someone tended #_2_Yuval a story"
    #x = "הגיע #_1_למישהו כי #_1_הוא #_1_הכין לא יפה"
    #y = "#_1_someone deserved it cause #_1_he really behaved badly"
    # y = "#_1_someone #_1_is not in the mood"
    # x = "#_1_מישהו לא במצב רוח"
    # y = "#_1_someone #_1_didn't feel well"
    # x = "#_1_מישהו לא #_1_הרגיש טוב"
    #x = "#_1_מישהו #_1_הלך לבית #_1_שלו"
    #y = "#_1_someone #_1_went to #_1_his house"
    #x = "#_1_מישהו #_1_הקריא לילד #_1_שלו סיפור"
    #y = "#_1_someone #_1_read #_1_his son a story"
    #x = "קוראים #_1_לו #_1_יובל ו#_1_הוא #_1_אהב חיות"
    #y = "#_1_his name is #_1_Yuval and #_1_he #_1_liked animals"
    #x = "ההורים #_1_שלמישהו קוראים #_1_לו סיפור לפני השינה"
    #y = "#_1_someone's parents read #_1_him a bedtime story"
    #x = "גרד #_1_למישהו בגב"
    #y = "#_1_someone's back itched"
    # x = "הטלפון הלך #_1_לוממש לאיבוד"
    # y = "#_1_hemms lost #_1_his phone"
    #x = "#_1_מישהו #_1_הכין #_1_לעצמו חביתה"
    #y = "#_1_someone #_1_made #_1_himself an omlete"
    # y = "make room to #_1_Meirav, #_2_Yuval's daughter"
    # x = "תעשה מקום ל#_1_מירב הבת #_2_שלו"
    #
    # x = "הטלפון #_1_שליובל הלך לאיבוד"
    # y = "#_1_Yuval lost #_1_his phone"
    #
    ##y = "#_1_someone #_1_wanted to talk to me"
    #(bad רצה) #x = "#_1_מישהו #_1_רצה לדבר איתי"
    x = "#_1_מישהו לא #_1_רצה לדבר אית#_2_ו"
    y = "#_1_someone #_1_didn't want to talk to #_2_him"
    x = "#_1_מישהו לא #_1_חשב על העתיד"
    y = "#_1_someone #_1_didn't think about the future"
    x = "#_1_מישהו #_1_הלך לקולנוע"
    y = "#_1_someone #_1_went to school"
    x = "#_1_אין #_1_למישהו מצב רוח"
    y = "#_1_someone #_1_is not in the mood"
    x = "#_1_מישהו #_1_צברח"
    y = "#_1_someone #_1_was upset"
    y = "#_1_someone #_1_read me a story"
    x = "#_1_מישהו #_1_הקריא לי סיפור"
    x = "קוראים #_1_לו #_1_יובל"
    y = "#_1_his name is #_1_Yuval"
    x = "קוראים #_1_לו למטה"
    y = "They are calling #_1_him downstairs"
    x = "קוראים #_1_לו סיפור"
    y = "They are reading #_1_him a story"
    x = "#_1_מישהו #_1_קרא #_2_לו סיפור לפני השינה"
    y = "#_1_someone #_1_read #_2_him a bedtime story"
    x = "#_1_מישהו #_1_אכל #_2_למישהו מהצלחת"
    y = "#_1_someone #_1_ate from #_2_someone's plate"
    y = "#_1_he #_1_ate from #_2_his plate"
    x = "#_1_הוא #_1_אכל מצלחת#_2_ו"
    y = "#_1_someone's back itches"
    x = "מגרד #_1_למישהו הגב"
    y = "they call #_1_him #_1_Yuval"
    x = "הם קוראים #_1_לו #_1_יובל"
    x = "תעש"
    x = "#_1_הוא #_1_פזם #_1_לעצמו שיר"
    y = "#_1_he #_1_sang #_1_himself a song"
    x = "#_1_הוא #_1_פזם #_2_למישהו שיר"
    y = "#_1_he #_1_sang a song to #_2_tosomeone"
    x = "הטלפון הלך #_1_למישהו לאיבוד"
    y = "#_1_someone's phone got lost"
    x = "#_1_מישהו #_1_נטה להפגע בקלות"
    y = "#_1_someone #_1_tended to get hurt easily"
    y = "#_1_someone #_1_believed in #_2_Yuval"
    x = "#_1_מישהו #_1_האמין ב#_2_יובל"
    x = "#_1_מישהו #_1_האמין #_2_למישהו"
    y = "#_1_someone #_1_believed #_2_tosomeone"
    y = "#_1_someone deserved it because #_1_he #_1_didn't behave well"
    x = "הגיע #_1_למישהו כי #_1_הוא #_1_התנהג לא יפה"
    x = "#_1_מישהו #_1_הצליח בחיים בזכות כוח הרצון #_1_שלו"
    y = "#_1_someone #_1_succeeded in life thanks to #_1_his will power"
    x = "#_1_מישהו #_1_הצליח בחיים בזכות כוח הרצון #_1_שלו"
    y = "#_1_someone #_1_succeeded in life thanks to #_1_his parents power"
    x = "לא #_1_התחשק #_1_למישהו לאכול"
    y = "#_1_someone #_1_didn't feel like eating"
    x = "לא אכפת #_1_למישהו"
    y = "#_1_someone #_1_didn't care"
    x = "לא #_1_פועל_שנה #_2_למישהו כלום"
    y = "#_1_someone #_1_didn't care about anything"
    x = "#_1_למישהו לא #_1_היהה אכפת מה #_2_מישהו #_2_אמר"
    y = "#_1_someone #_1_didn't care about what #_2_someone #_2_said"
    x = "#_1_אין #_1_למישהו כוח היום ללמוד"
    y = "#_1_someone #_1_didn't feel like studying today"
    x = "#_1_מישהו #_1_השתגע כי #_1_הוא #_1_היה כל הלילה במקלט"
    y = "#_1_someone #_1_got crazy cause #_1_he #_1_was in the shelter all night"

    __black_list = []
    __sentences = zip(populate_pattern(x, "hebrew", ("צבר", "צובר")), populate_pattern(y, "english", None))
    __sentences = set(__sentences)
    for __sent1, __sent2 in __sentences:
        print(f"{__sent1}\n{__sent2}\n\n")
