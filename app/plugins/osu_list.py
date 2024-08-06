from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore


def osu_ordered_list(state: StateCore) -> None:
    for token in state.tokens:
        if token.type != "ordered_list_open":
            continue

        start_attr = token.attrGet("start")
        start = 0

        if start_attr is not None:
            start = int(start_attr) - 1
            token.attrs.pop("start")

        token.attrSet("style", f"--list-start: {start}")


def osu_list_plugin(md: MarkdownIt) -> None:
    md.core.ruler.push("osu_ordered_list", osu_ordered_list)
