from typing import Callable, Set

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore


def anchors_plugin(
    md: MarkdownIt,
    min_level: int = 1,
    max_level: int = 2,
    slug_func: Callable[[str], str] | None = None,
) -> None:
    selected_levels = list(range(min_level, max_level + 1))
    md.core.ruler.push(
        "anchor",
        _make_anchors_func(
            selected_levels,
            slug_func or slugify,
        ),
    )


def _make_anchors_func(
    selected_levels: list[int],
    slug_func: Callable[[str], str],
) -> Callable[[StateCore], None]:
    def _anchor_func(state: StateCore):
        slugs: Set[str] = set()

        for idx, token in enumerate(state.tokens):
            if token.type != "heading_open":
                continue

            level = int(token.tag[1])

            if level not in selected_levels:
                continue

            inline_token = state.tokens[idx + 1]
            assert inline_token.children is not None

            title = "".join(
                child.content
                for child in inline_token.children
                if child.type in ["text", "code_inline"]
            )

            # Check if there is an explicit id in curly braces at the end
            if not title.endswith("}") and "{" not in title:
                slug = unique_slug(slug_func(title), slugs)
                token.attrSet("id", slug)

                continue

            title, attr_content = title.rsplit("{", 1)

            # Remove "id=" or "#" from the explicit_id
            explicit_id = attr_content.rstrip("}").lstrip("id=").lstrip("#")

            # Set the id attribute to the explicit_id
            token.attrSet("id", explicit_id)

            # Update the inline token content
            inline_token.children[0].content = title

    return _anchor_func


def slugify(title: str) -> str:
    return title.strip().lower().replace(" ", "-")


def unique_slug(slug: str, slugs: Set[str]) -> str:
    uniq = slug
    i = 1
    while uniq in slugs:
        uniq = f"{slug}.{i}"
        i += 1
    slugs.add(uniq)
    return uniq
