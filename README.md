# nlp_patterns_db

## Background
In order to test the ability of translation system to generalize well from Hebrew to English, we need a large data set
of simple Hebrew-English parallel sentences.
In this repository you can find the following:
* Patterns populater - given a parallel pattern in Hebrew and English, populates them in differet tesnses and "Actors", e.g.
"#_1_someone #_1_called #_2_someone+obj", "#_1_מישהו #_1_קרא #_2_למישהו" 
would be populated, resulting in:
* I called the woman, אני קראתי לאישה
* I called the child, אני קראתי לילד
* I call the woman, אני קורא לאישה
* I call the child, אני קורא לילד
* She called the woman, היא קראה לאישה
* She called the child, היא קראה לילד
* She calls the woman, היא קוראת לאישה
* She calls the child, היא קוראת לילד
* ...


## Installation
TODO

# Introduction
The project provides a pattern populater - you provide a sentence in Hebrew/ English, using the following rules:
Each replaced word is annotated using <PREFIX>#\_<SPEAKER_NUMBER>\_<EXTRA_ANNOTATION>\_\<WORD\>, where
* PREFIX: alphabet letters.
* SPEAKER_NUMBER: integer. If only one speaker in the sentence use only 1 as a speaker. If two, use 1 & 2 etc...
* EXTRA_ANNOTATION: TODO explain, more complicated.
* WORD: 
  
  -> verb: should be in the form of "he-past" both English and Hebrew, e.g. "walked", "הלך".
  
  -> magic words: someone, his, him, someone+obj, Yuval, Amos, Meirav, מישהו, למישהו, היה+יהיה, שלו. You can find their corresponding replacements in file: TODO.

## Examples
* #_1_someone #_1_went to school.
** someone is a magic word, and would be replaced with "He, She, ... The child, The woman....".
** Note that both 'someone' and 'went' are annotated with #_1_ => same SPEAKER_NUMBER, since they both
  refer to the same speaker. That allows us to make them agree on gender, tense... think about the following pattern:
  #_1_someone #_1_deserved it cause #_2_someone #_2_annoyed #_1_him
  This pattern will generate the many combinations, e.g.
  * The child deserved it cause we **annoyed** him.
  * The child **deserves** it cause we **annoyed** him.
  * The child **deserved** it cause we **annoy** him.

Known issues:
1. patterns like "#_1_someone #_1_made #_2_someoneobj an omlete" generates
also "I made **me** an omblete", instead of "I mande **myself** an omlete" (also generates "She made her an omblete", where but that's ok).

2. No support yet for Hebrew imperative "#_1_עתיד_עשה ל#_1_מירב, בת#_2_ו, מקום"
(in this example "תעשי", "תעשו", "תעשה")
