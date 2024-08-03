from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore


def osu_list(state: StateCore) -> None:
    for token in state.tokens:
        if token.type != "ordered_list_open":
            continue

        start = token.attrGet("start")

        if start is None:
            start = 0
        else:
            start -= 1
            token.attrs.pop("start")

        token.attrSet("style", f"--list-start: {start}")


def osu_list_plugin(md: MarkdownIt) -> None:
    md.core.ruler.push("osu_list", osu_list)
