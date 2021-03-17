from typing import Sequence, List, Dict
from pprint import pprint
from annotated_word import Word
import re
from replacements_provider import get_word_replacements_hebrew, get_word_replacements_english
def get_word_replacements(word: Word, gender, tense, lang="hebrew"):
    if lang == "hebrew":
        return get_word_replacements_hebrew(word, gender, tense)
    return get_word_replacements_english(word, gender, tense)

POAL = "פועל"

F = ["F"]
M = ["M"]
MF = F + M
FM = M + F





def populate_li(patten: str) -> Sequence[str]:
    return [patten.replace("$לי", alternative) for alternative in li_list]


def populate_actor_plays(patten: str) -> Sequence[str]:
    words = patten.split()
    verb = ""
    for i, word in enumerate(words):
        if word == "$פועל":
            verb = words[i+1]
    instances = []
    for category_index, category_actors in enumerate(actors):
        for actor in category_actors:
            instances.append(patten.replace("$משחק", actor).replace(verb, "").replace("$פועל", verbs[verb][category_index]))

    return instances

def populate_mine(pattern: str) -> Sequence[str]:
    return [pattern.replace("$שלי", alternative) for alternative in my_list]


def populate_oti(pattern: str) -> Sequence[str]:
    return [pattern.replace("$אותי", alternative) for alternative in aoti_list]

def populate_name(pattern: str) -> Sequence[str]:
    return [pattern.replace("$שם", alternative[0]) for alternative in names]


def get_priority(word_type):
    if word_type == "MAGIC":
        return 0
    if word_type == "POAL":
        return 1
    return 2


def annotate_word(word: str, word_pos) -> Word:
    groups: List[int] = list(re.findall("#_([0-9]+)", word))
    assert len(groups) <= 1, f"Bad annotation for word: {word}"
    if not groups:
        return Word(word, word_pos=word_pos)
    group = groups[0]
    content = list(re.split("#_[0-9]+", word)[1].split("_"))
    prefix = re.split("#_[0-9]+", word)[0]
    w = Word(word, int(group), role=content[-1], word_pos=word_pos, prefix=prefix)
    attrs = [attr for attr in content[:-1] if attr]
    if POAL in attrs:
        w.type = POAL
    else:
        w.type = "Magic"
    return w


from collections import defaultdict
def get_implicit_pron_by_gender(gender):
    d = defaultdict(str)
    d.update({"She": "היא", "He": "הוא"})
    return d[gender]

from typing import Set
import nltk
def process_sentence(sent: str):

    words = nltk.WordPunctTokenizer().tokenize(sent.replace("#", "אבגדה"))
    words = [word.replace("אבגדה", "#") for word in words]
    annotated_words = [annotate_word(word, i) for i, word in enumerate(words)]

    groups: Set[int] = {word.group for word in annotated_words}
    import itertools
    all_groups_combs = []
    for group in groups:
        group_words = [word for word in annotated_words if word.group == group]
        group_combs = []
        for gender, tense in [("She", "PRESENT"), ("He", "PRESENT"), ("We", "PRESENT"), ("I",                                                                  "PRESENT")]:
            all_word_reps = []
            for word in group_words:
                word_reps = get_word_replacements(word, gender, tense)
                new_words = [(word_rep, word.word_pos) for word_rep in word_reps]
                all_word_reps.append(new_words)

            for var in itertools.product(*all_word_reps):
                group_com = list(var)
                group_combs.append(group_com)
        all_groups_combs.append(group_combs)
    all_sentences = set()
    for var in itertools.product(*all_groups_combs):
        sent = list(itertools.chain(*list(var)))
        sent = [y[0] for y in sorted(sent, key=lambda x: x[1])]
        all_sentences.add(tuple(sent))

    all_sentences = [sent for sent in all_sentences if "בני של" not in sent]

    all_sentences = get_non_name_contradicting_sentences(all_sentences, annotated_words)
    all_sentences_text = []
    for sent in all_sentences:
        all_sentences_text.append(
        " ".join([annotated_words[i].prefix + word for i, word in enumerate(sent)])
        )
    return [sent.replace(" .", ".").replace(" ,", ",").replace(" !", "!").replace(" ?", "?") for sent in
            all_sentences_text]

import itertools
def get_non_name_contradicting_sentences(all_sentences, annotated_words):
    group_name_indices = defaultdict(list)
    for word in annotated_words:
        if word.role == "עמוס" or word.role == "יובל":
            group_name_indices[word.group].append(word.word_pos)

    must_different_names_pairs = []
    for comb in itertools.combinations(group_name_indices.values(), 2):
        must_different_names_pairs.extend(list(itertools.product(*comb)))

    sentences_to_remove = set()
    for s_id, sent in enumerate(all_sentences):
        for pair in must_different_names_pairs:
            if sent[pair[0]] == sent[pair[1]]:
                sentences_to_remove.add(s_id)
    return [sent for s_id, sent in enumerate(all_sentences) if s_id not in sentences_to_remove]
    # sentences_to_remove = set()
    # for s_id, sent in enumerate(all_sentences):
    #     for group, indices in group_name_indices.items():
    #         if len(indices) > 1:
    #             words = [sent[index] for index in indices]
    #             if len(set(words)) != 1:
    #                 sentences_to_remove.add(s_id)




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
    s = "קוראים #_1_לו #_1_יובל"
    s = "ההורים #_1_שלו קוראים #_2_לו-ממש סיפור לפני השינה"
    s = "#_1_אכל #_2_לו-ממש מהצלחת"
    s = "מגרד #_2_לו בגב"
    s = "הראש #_1_שלו מגרש"
    s = "מכנים אותי #_1_יובל"
    s = "תעשה ל#_1_עמוס בנו של #_2_עמוס בבקשה #_1_עמוס"
    s = "#_1_פועל_גרד בראש"
    s = "תעשה ל#_1_מירב , בתו של #_2_עמוס , מקום"
    from pprint import pprint
    x = "תעשה ל#_1_מירב, בתו של #_2_עמוס. מקום"
    x = "#_1_ציר לי כבשה!"
    x = "#_1_פזם לעצמ#_1_ו שיר"
    x = "#_1_הכין #_1_לוממש חביתה"
    x = "הטלפון הלך #_2_לו לאיבוד"
    x = "#_1_הוא #_1_נטה להפגע בקלות"
    x = "#_1_הוא #_1_האמין ב#_2_יובל"
    x = "הגיע #_1_לו כי #_1_הואממש #_1_התנהג לא יפה"
    x = "#_1_הוא #_1_הצליח בחיים בזכות הרצון #_1_שלו"
    x = "ל#_1_עמוס לא משנה מה #_2_עמוס, בנו הקטן, יגיד"
    x = "לא #_1_האמין לאף אחד"
    x = "#_1_הוא לא #_1_ראה דבר כזה מימי#_1_ו"
    pprint(process_sentence(x))
    a = 3