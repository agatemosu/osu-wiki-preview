import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

from scripts.get_flag_codepoint import get_flag_codepoint


def get_flag_url(flagCodepoint: str) -> str:
    return f"/assets/images/flags/{flagCodepoint}.svg"


def inline_flag(state: StateInline, _: bool) -> bool:
    pos = state.pos

    if (
        pos + 3 >= state.posMax
        or ord(state.src[pos]) != 0x3A  # :
        or ord(state.src[pos + 1]) != 0x3A  # :
        or ord(state.src[pos + 2]) != 0x7B  # {
    ):
        return False

    match = re.match(r"^::{\s+flag=([A-Z]{2})\s+}::", state.src[pos:])

    if not match:
        return False

    flag_codepoint = get_flag_codepoint(match.group(1))

    # Add a token for the custom syntax
    token = state.push("flag_open", "span", 1)
    token.attrs = {
        "class": "flag-country flag-country--wiki",
        "style": f"background-image: url('{get_flag_url(flag_codepoint)}')",
    }

    state.push("flag_close", "span", -1)
    state.pos += len(match.group(0))

    return True


def flag_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.after("text", "flag", inline_flag)
