from utils import *


def load_verbs_from_json():
    import json
    arabic_dict = json.load(open('data/arabic_dict.json', "r"))
    for canonical_verb in arabic_dict.keys():
        future = arabic_dict[canonical_verb]['FUTURE']
        arabic_dict[canonical_verb]['PRESENT'] = future  # in arabic future and present are the same

    return arabic_dict


class ArabicTransformer:
    from camel_tools.morphology.generator import MorphologyDB
    db_reinflect = MorphologyDB.builtin_db(flags='r')
    db_analyze = MorphologyDB.builtin_db()
    def __init__(self):
        from camel_tools.morphology.reinflector import Reinflector
        from camel_tools.morphology.generator import Generator
        from camel_tools.morphology.analyzer import Analyzer

        # import os
        # os.environ['CAMELTOOLS_DATA'] = '/home/orgersh/.camel_tools'

        import subprocess
        # !export | camel_data light

        # self.generator = Generator(MorphologyDB.builtin_db(flags='g'))
        self.analyzer = Analyzer(ArabicTransformer.db_analyze)
        self.reinflector = Reinflector(ArabicTransformer.db_reinflect)

    def reinflect(self, canonical_form: str, tense: Tense = Tense.PAST, gender: Gender = Gender.HE, is_active=True):
        from camel_tools.utils.dediac import dediac_ar

        feats = ArabicTransformer.gender_to_features(gender)
        feats.update(ArabicTransformer.feats_by_tense(tense))
        feats['vox'] = 'a' if is_active else 'p'

        results = self.reinflector.reinflect(canonical_form, feats)
        dediac_res = [dediac_ar(res['diac']) for res in results]
        dediac_res = set(dediac_res)
        if not dediac_res:
            print(f"NO data for base : {canonical_form}, gender : {gender}, tense : {tense}")
            exit(1)
        return dediac_res.pop() # not handeling the case where there are 2 or more options



    def analyze(self, canonical_form: str):

        # feats = ArabicTransformer.gender_to_features(gender)
        # if tense is not Tense.PAST:
        #     feats['prc1'] = 'sa_fut'
        #     feats['asp'] = 'i'
        #
        # analyses = self.analyzer.analyze(canonical_form)
        return self.analyzer.analyze(canonical_form)[-1]


    @staticmethod
    def gender_to_features(gender: Gender):

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
            gen = 'f'
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
            gen = 'f'
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
    def feats_by_tense(tense : Tense):

        present = \
            {
                'asp': 'i',
                'mod': 'u',
            }
        future = \
            {
                'asp': 'i',
                'mod': 'u',
                'prc1': 'sa_fut'
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
        return present

if __name__ == '__main__':

     transformer = ArabicTransformer()
     # for a in transformer.reinflect('كَتَبَ', Tense.FUTURE, Gender.SHE):
     #     print(a)
     feats1 = transformer.analyze("تهرب")
     feats2 = transformer.analyze("هرب")
     #

     for feat_key in feats1.keys():
         if feats1[feat_key] != feats2[feat_key] or feat_key == 'catib6':
             print(f"Field {feat_key}, Future form = {feats1[feat_key]}, Past form = {feats2[feat_key]}")
