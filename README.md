# nlp_patterns_db

## Background
In order to test the ability of translation system to generalize well from Hebrew to English, we need a large data set
of simple Hebrew-English parallel sentences. Most of the work presented here is the engineering part, since the current used translation model is very weak, so the bleu scores are not represetitive.

### Patterns populater (patterns_populator.py)
Given a parallel pattern in Hebrew and English, populates them in differet tesnses and "Actors", e.g.
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

#### patterns format
The general token pattern is \[unchanged-prefix\]#\_\<actor_index\>\_\[\ANNOTATION\_\]<verb|magic_word>.

##### unchanged-prefix 
the annotator pastes this part to the popultaed pattern. For example: "צלחת#_1_ו" would result in:
* צלחתו
* צלחתי
* צלחתנו
* צלחתם
* ...
(Since the "ו" is a magic word, and the "צלחת" is a prefix).

##### actor_index
tells the populator which tokens should be kept in sync in terms of gender and tense. E.g. "#_1_someone #_1_walked" would result in: 
* The child walked
* The child walks
* The chils will walk
* I walked
* I walk
* ...
While #_1_someone #_2_walked will result in:
* The child **walk**
* The child walks
* I walk
* I walk**s**

##### magic_word
A word with defined replacements, In order that matches between languages. For example

"Someone" ->
* He
* The child
* She
* The woman
* I
* ...

"Someone+obj" ->
* him
* him
* her
* her
* me

"מישהו" -> 
* הוא
* הילד
* היא
* האישה
* אני

"עם+מישהו" ->
* איתו
* איתו
* איתה
* איתה
* איתי


### Populate patterns and run translation: main.py
Popultes the patterns given in the input file, translate them to English using a simple vanilla model, and computes the bleu score.

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
