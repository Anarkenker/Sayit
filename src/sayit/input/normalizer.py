import re


def normalize_text(text: str) -> str:
    text = text.strip()
    text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_surface_facts(text: str) -> dict[str, list[str]]:
    return {
        "numbers": re.findall(r"\d+(?:\.\d+)?", text),
        "dates": re.findall(r"(今天|明天|后天|本周|下周|周[一二三四五六日天]|\d+月\d+日)", text),
        "amounts": re.findall(r"(?:¥|￥|\$)?\d+(?:\.\d+)?(?:元|块|w|k)?", text),
        "urls": re.findall(r"https?://\S+", text),
    }
