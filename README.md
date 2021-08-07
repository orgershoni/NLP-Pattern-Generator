# nlp_patterns_db
Should generally install nodebox_linguistics_extended package (currently copied it to a directory in this repository)
https://github.com/RensaProject/nodebox_linguistics_extended

Known issues:
1. patterns like "#_1_someone #_1_made #_2_someoneobj an omlete" generates
also "I made **me** an omblete", instead of "I mande **myself** an omlete" (also generates "She made her an omblete", where but that's ok).

requirements:
wheel
pandas
nltk
sgmllib3k
