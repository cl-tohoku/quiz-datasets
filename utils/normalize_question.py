import re
import sys
import unicodedata


def normalize_question(text):
    # substitute some symbols that will not be replaced by unicode normalization
    text = text.replace("～", "〜")

    # unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # removal of bracketed subtexts
    text = re.sub(r"【.*?】", "", text)
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\(.*?\)", "", text)

    # compress whitespaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


if __name__ == "__main__":
    for line in sys.stdin:
        print(normalize_question(line))
