import re
from typing import Dict, List
from collections import defaultdict

def remove_diacritics(word):
    return re.sub("[\u0590-\u05CF]", "", word)


def get_tense(verb_attrs: List[str]):
    if "PAST" in verb_attrs:
        return "PAST"
    if "FUTURE" in verb_attrs:
        return "FUTURE"
    if "PRESENT" in verb_attrs:
        return "PRESENT"
    return ""


def get_gender(verb_attrs: List[str]):
    if "F" in verb_attrs and "SINGULAR" in verb_attrs and "THIRD" in verb_attrs:
        return "She"
    if "M" in verb_attrs and "SINGULAR" in verb_attrs and "THIRD" in verb_attrs:
        return "He"
    if "FIRST" in verb_attrs and "SINGULAR" in verb_attrs:
        return "I"
    if "FIRST" in verb_attrs and "PLURAL" in verb_attrs:
        return "We"
    return ""


def add_verb_record(record: str, verbs: Dict):
    attrs = remove_diacritics(record).split(",")
    verb = attrs[-1]
    content = attrs[2]
    metadata = attrs[3].split("+")
    if verb not in verbs:
        verbs[verb] = defaultdict(defaultdict)

    verb_record = verbs[verb]
    tense = get_tense(metadata)
    gender = get_gender(metadata)
    if not tense or not gender:
        return
    verb_record[tense][gender] = content


def create_verbs_table(verbs_table_path: str):
    from pathlib import Path
    data = Path(verbs_table_path).read_text(encoding="utf-8")
    lines = list(data.splitlines())[1:]
    verbs = {}
    for line in lines:
        add_verb_record(line, verbs)
    return verbs
