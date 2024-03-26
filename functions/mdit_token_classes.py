from markdown_it import MarkdownIt
from markdown_it.token import Token


def set_token_classes(tokens: list[Token], mapping: dict[str, list[str]]) -> None:
    for token in tokens:
        is_opening_tag = token.nesting != -1

        if is_opening_tag and token.tag in mapping:
            existing_class_attribute = token.attrGet("class") or ""

            existing_classes = existing_class_attribute.split(" ")
            given_classes = mapping.get(token.tag, "")

            new_classes = existing_classes + given_classes

            token.attrSet("class", " ".join(new_classes).strip())

        if token.children:
            set_token_classes(token.children, mapping)


def tag_class_plugin(md: MarkdownIt, mapping: dict[str, list[str]]) -> None:
    md.core.ruler.push(
        "tag_class", lambda state: set_token_classes(state.tokens, mapping)
    )
