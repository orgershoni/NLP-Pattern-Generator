from utils import *


# def load_verbs_from_json():
#     import json
#     arabic_dict = json.load(open('data/arabic_dict.json', "r"))
#     for canonical_verb in arabic_dict.keys():
#         future = arabic_dict[canonical_verb]['FUTURE']
#         arabic_dict[canonical_verb]['PRESENT'] = future  # in data future and present are the same
#
#     return arabic_dict


def resolve_db_path():
    from pathlib import Path
    path = Path(__file__).parent
    rel_dirs = [dir.name for dir in path.iterdir() if dir.is_dir()]
    while 'data' not in rel_dirs:
        path = path.parent
        rel_dirs = [dir.name for dir in path.iterdir() if dir.is_dir()]

    return str(path / 'data' / 'arabic_db')


class ArabicTransformer:
    db_reinflect = None
    db_analyze = None

    # init env
    import os
    os.environ['CAMELTOOLS_DATA'] = resolve_db_path()

    def __init__(self):
        from camel_tools.morphology.reinflector import Reinflector
        from camel_tools.morphology.generator import Generator
        from camel_tools.morphology.analyzer import Analyzer
        from camel_tools.morphology.generator import MorphologyDB

        if not ArabicTransformer.db_reinflect:  # avoid multiple init of
                                                # static members
            ArabicTransformer.db_reinflect = MorphologyDB.builtin_db(flags='r')
            ArabicTransformer.db_analyze = MorphologyDB.builtin_db()

        self.analyzer = Analyzer(ArabicTransformer.db_analyze)
        self.reinflector = Reinflector(ArabicTransformer.db_reinflect)

    def get_pos(self, canonical_form: str):
        analysis = self.analyze(canonical_form)
        return analysis['pos']

    def is_possessive(self, canonical_form: str):
        analysis = self.analyze(canonical_form)
        return 'poss' in analysis['enc0']

    def reinflect(self, canonical_form: str, gender: Gender = Gender.HE,
                  is_active: bool = True, tense: Tense = None,
                  dediac: bool = True, force_single_output = True, meaning=None):
        from camel_tools.utils.dediac import dediac_ar

        is_possessive = self.is_possessive(canonical_form)
        if self.get_pos(canonical_form) == 'noun' or not tense:
            if is_possessive:
                feats = self.get_features_for_possessive_noun(gender)
            else:
                feats = self.get_features_for_noun(gender)
        else:
            feats = self.get_feats_for_verb(gender, tense, is_active)

        # results = self._reinflect(canonical_form, feats, dediac)
        results = self.reinflector.reinflect(canonical_form, feats)

        if meaning:
          for result in results:
            if result['stemgloss'] == meaning:
              return [dediac_ar(result['diac'])]
        #   print(f"No result with meaning {meaning} was found")
        #   print(*results,sep = '\n')

        if force_single_output and results:
            return [dediac_ar(results.pop()['diac'])]

        return list(results)

    def get_feats_for_verb(self, gender: Gender,
                           tense: Tense, is_active: bool=True):

        feats = ArabicTransformer._gender_to_features(gender)
        feats.update(ArabicTransformer.feats_by_tense(tense))
        feats['vox'] = 'a' if is_active else 'p'

        return feats

    def _reinflect(self, canonical_form, feats, dediac: bool):

        from camel_tools.utils.dediac import dediac_ar
        results = self.reinflector.reinflect(canonical_form, feats)
        if dediac:
            results = [dediac_ar(res['diac']) for res in results]
        else:
            results = [res['diac'] for res in results]

        results = set(results)    # Maybe useful to remove duplicates
        # in case of dediac

        return results

    def analyze(self, canonical_form: str, single_output=True):

        # feats = ArabicTransformer.gender_to_features(gender)
        # if tense is not Tense.PAST:
        #     feats['prc1'] = 'sa_fut'
        #     feats['asp'] = 'i'
        #
        # analyses = self.analyzer.analyze(canonical_form)
        analyses = self.analyzer.analyze(canonical_form)
        return analyses.pop() if single_output else analyses

    @staticmethod
    def _gender_to_features(gender: Gender):

        gen = ""
        num = ""
        person = ""
        if gender == Gender.HE:
            gen = 'm'
            num = 's'
            person = '3'
        if gender == Gender.SHE:
            gen = 'f'
            num = 's'
            person = '3'
        if gender == Gender.WE_F:
            gen = 'm'
            num = 'p'
            person = '1'
        if gender == Gender.WE_M:
            gen = 'm'
            num = 'p'
            person = '1'
        if gender == Gender.THEY:
            gen = 'm'
            num = 'p'
            person = '3'
        if gender == Gender.I_F:
            gen = 'm'
            num = 's'
            person = '1'
        if gender == Gender.I_M:
            gen = 'm'
            num = 's'
            person = '1'
        if gender == Gender.YOU:
            gen = 'm'
            num = 's'
            person = '2'

        return {
            'gen': gen,
            'num': num,
            'per': person
        }

    @staticmethod
    def get_features_for_possessive_noun(gender: Gender):

        feats = ArabicTransformer._gender_to_features(gender)

        if feats['per'] == '1': # in arabic no need for gender in 1st person
            enc0 = f"{feats['per']}{feats['num']}_poss"
        else:
            enc0 = f"{feats['per']}{feats['gen']}{feats['num']}_poss"

        return {'enc0': enc0, 'prc0': '0'}

    @staticmethod
    def get_features_for_noun(gender: Gender):

        feats = ArabicTransformer._gender_to_features(gender)
        del feats['per']
        return feats

    @staticmethod
    def feats_by_tense(tense: Tense):

        present = \
            {
                'asp': 'i',
                'mod': 'u',
            }
        future = \
            {
                'asp': 'i',
                'mod': 'u',
                # 'prc1': 'sa_fut'
            }
        past = \
        {
            'asp': 'p',
            'mod': 'i',
        }

        if tense == Tense.PAST:
            return past
        elif tense == Tense.FUTURE:
            return future
        elif tense == Tense.PRESENT:
            return present
        return {}
    
    def disambiguation(self, base_form : str, context : str = ""):

      def get_user_input(options, base_form : str):

        msg = ''.join(options)
        context_str = f"in the pattern {encode_arabic(context)}" if context else ""
        print(f"The word you entered as token {context_str} is ambigous.")
        print(f"Please choose the meaning of {encode_arabic(base_form)} you aimed for entering an index")

        idx = int(input(msg))
        while not 0 <= idx < len(options):
          print("idx out of bounds, try again.")
          idx = int(input(msg))
        print(f"You chose the meaning {options[idx]}")
        return idx

      analyses = list(self.analyze(base_form, single_output=False))
      meanings = sorted(list(set([props['stemgloss'] for props in analyses])))
      if len(meanings) > 1:
        options = [f"{idx} : {meaning}\n" for idx,meaning in enumerate(meanings)]
        user_input_idx = get_user_input(options, base_form)
        
        meaning = meanings[user_input_idx]
        for analysis in analyses:
          if analysis['stemgloss'] == meaning:
            return analysis
      return None


def test_analyze():

    transformer = ArabicTransformer()

    feats1 = transformer.analyze("جبهتنا")
    feats2 = transformer.analyze("جبهته")

    print(feats1)
    print(feats2)

    for feat_key in feats1.keys():
        if feats1[feat_key] != feats2[feat_key]:
            print(f"Field {feat_key}, Future form = {feats1[feat_key]}, Past form = {feats2[feat_key]}")


def test_reinflection():

    transformer = ArabicTransformer()

    base_forms = ['هَرَّبَ', 'رجع', 'قال', 'حبّ', 'جبهة']
    count_failures = 0
    for base_form in base_forms:
        for gender in Gender:
            for tense in Tense:

                reinflections = transformer.reinflect(base_form, gender,
                                                      tense=tense)
                if not reinflections:
                    reinflections = ['NO_REINFLECTION FOUND']
                    count_failures += 1

                more_than_single_output = type(reinflections) != str and \
                                          len(reinflections) > 1

                if not more_than_single_output:
                    reinflections = [reinflections]

                if more_than_single_output:
                    print("#MORE THAT ONE OPTION#")
                for reinflection in reinflections:
                    print(f"base form : {base_form}, gender : {gender}, tense "
                          f"{tense}, reinflection : {reinflection}")
                if more_than_single_output:
                    print("#END#")
    print(f"failed in {count_failures} reinflections")


if __name__ == '__main__':

    test_analyze()
    test_reinflection()