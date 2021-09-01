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

##### verb
Verb in the form "he-past" (e.g. "הלך", "walked").

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

"ו" ->
* ו
* ו
* ה
* ה
* י

##### annotation
* "M"/ "ז" - tells the populator to treat the verb as if it was always in the form of "He".

E.g. "הראש #_1_ז_כאב #_2_למישהו" would result in
הראש כאב לעמרי
הראש כאב לאישה
...
and avoid emitting:
הראש כאבה לעמרי
הראש כואבים לעמרי

* "F"/ "נ" - tells the populator to treat the verb as if it was always in the form of "SHe".



### Populate patterns and run translation: main.py
Popultes the patterns given in the input file, translate them to English using a simple vanilla model, and computes the bleu score.

## Installation
Currently only working from huji environment (using absolute paths for the translation model), but the patterns generator should work from any python3 env.
* Use the requirements file to install needed packages.
* Note that the "nodebox_linguistics_extended" dir is an external library that I copied into this repository because
its installation is sometimes problematic, should call "python setup.py" after "cd" to the directory.

## Work in progress
1. patterns like "#_1_someone #_1_made #_2_someoneobj an omlete" generates
also "I made **me** an omblete", instead of "I made **myself** an omlete".

2. No support yet for Hebrew imperative "#_1_עתיד_עשה ל#_1_מירב, בת#_2_ו, מקום"
(in this example "תעשי", "תעשו", "תעשה")

3. Correct ordering of parallel sentences where the actor is different in each language, e.g.:
* I missed him
* הוא חסר לי
