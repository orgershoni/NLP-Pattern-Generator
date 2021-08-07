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
        if "F" in verb_attrs:
            return "I_F"
        elif "M" in verb_attrs:
            return "I_M"
        elif "MF" in verb_attrs:
            return "I_MF"
        else:
            raise RuntimeError("Unexpected hebrew verb record found: %s" % verb_attrs)
    if "FIRST" in verb_attrs and "PLURAL" in verb_attrs:
        if "F" in verb_attrs:
            return "WE_F"
        elif "M" in verb_attrs:
            return "WE_M"
        elif "MF" in verb_attrs:
            return "WE_MF"
        else:
            raise RuntimeError("Unexpected hebrew verb record found")
    return ""


def _add_verb_record(record: str, verbs: Dict, canonical_verb):
    attrs = remove_diacritics(record).split(",")
    content = attrs[2]
    metadata = attrs[3].split("+")
    if canonical_verb not in verbs:
        verbs[canonical_verb] = defaultdict(defaultdict)

    verb_record = verbs[canonical_verb]
    tense = get_tense(metadata)
    gender = get_gender(metadata)
    if not tense or not gender:
        return
    if gender.endswith("_MF"):
        gender = gender[:-3]
        if gender + "_M" not in verb_record[tense]:
            verb_record[tense][gender + "_M"] = content
        if gender + "_F" not in verb_record[tense]:
            verb_record[tense][gender + "_F"] = content
    else:
        # Prefer first occurrence, still need to verify it's actually better.
        if gender not in verb_record[tense]:
            verb_record[tense][gender] = content


def add_verb_record(record: str, verbs: Dict):
    canonical_verb_with_diacritics = record.split(",")[-1]
    canonical_verb_no_diacritics = remove_diacritics(record).split(",")[-1]
    _add_verb_record(record, verbs, canonical_verb_no_diacritics)
    _add_verb_record(record, verbs, canonical_verb_with_diacritics)


def create_verbs_table(verbs_table_path: str):
    from pathlib import Path
    data = Path(verbs_table_path).read_text(encoding="utf-8")
    lines = list(data.splitlines())[1:]
    verbs = {}
    for line in lines:
        add_verb_record(line, verbs)
    return verbs
