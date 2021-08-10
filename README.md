# nlp_patterns_db

## Installation
1. Should generally install nodebox_linguistics_extended package (currently copied it to a directory in this repository)
https://github.com/RensaProject/nodebox_linguistics_extended
### requirements
wheel
pandas
nltk
sgmllib3k

# Introduction
The project provides a pattern populater - you provide a sentence in Hebrew/ English, using the following rules:
Each replaced word is annotated using <PREFIX>#\_<SPEAKER_NUMBER>\_<EXTRA_ANNOTATION>\_\<WORD\>, where
* PREFIX: alphabet letters.
* SPEAKER_NUMBER: integer. If only one speaker in the sentence use only 1 as a speaker. If two, use 1 & 2 etc...
* EXTRA_ANNOTATION: TODO explain, more complicated.
* WORD: normal word, or a magic word, below you can see the allowed magic words.

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

