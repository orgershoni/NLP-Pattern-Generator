import os


def _get_translated_sentences():
    with open("/cs/snapless/oabend/borgr/TG/en-he/output/tmp_omrygilon2.out", "r") as f:
        return f.read().splitlines()


def translate(text: str):
    with open("/cs/snapless/oabend/borgr/SSMT/data/en_he/omrygilon_generalization/test_he.he", "w") as f:
        f.write(text)
    os.system("rm -f /cs/snapless/oabend/borgr/SSMT/preprocess/data/en_he/20.07.21/omrygilon_generalization/test_he.tok.he")
    os.system("/cs/snapless/oabend/borgr/SSMT/preprocess/preprocess_challenges_pretrained_omrygilon.sh > /dev/null 2>&1")
    os.system("/cs/snapless/oabend/borgr/TG/en-he/scripts/translate_seq_omrygilon.sh >/dev/null 2>&1")
    os.system("cat /cs/snapless/oabend/borgr/TG/en-he/output/tmp_omrygilon2.out")
    return _get_translated_sentences()


def _interactive_translate():
    text = input("Enter a sentence in Hebrew\n")
    translate(text)
    print(translate(text))


if __name__ == "__main__":
    _interactive_translate()
