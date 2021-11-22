def load_verbs_from_json():
    import json
    arabic_dict = json.load(open('data/arabic_dict.json', "r"))
    for canonical_verb in arabic_dict.keys():
        future = arabic_dict[canonical_verb]['FUTURE']
        arabic_dict[canonical_verb]['PRESENT'] = future  # in arabic future and present are the same

    return arabic_dict
