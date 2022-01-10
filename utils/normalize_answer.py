import re
import sys
import unicodedata


def normalize_answer(text):
    # substitute some symbols that will not be replaced by unicode normalization
    text = text.replace("～", "〜")

    # unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # removal of bracketed subtexts
    text = re.sub(r"【.*?】", "", text).strip() or text
    text = re.sub(r"\(.*?\)", "", text).strip() or text
    text = re.sub(r"\[.*?\]", "", text).strip() or text

    # removal of annotation beginnig with "※"
    if "※" in text:
        text = text[:text.index("※")]

    # removal of annotation beginnig with a comma or slash
    text = text.strip()
    if text[0] not in "「『":
        text = re.sub(r"[、/].+$", "", text)

    # removal of kagi-kakkos
    text = re.sub(r"「(.*?)」", r"\1", text)
    text = re.sub(r"『(.*?)』(.*)", r"\1", text)  # 『〇〇』シリーズ → 〇〇

    # compress whitespaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


if __name__ == "__main__":
    for line in sys.stdin:
        print(normalize_answer(line))
