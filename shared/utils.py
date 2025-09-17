from urllib.parse import quote


def encode_tag(tag: str) -> str:
    return quote(tag, safe="")
