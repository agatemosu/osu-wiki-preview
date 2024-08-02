from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.rules_core import StateCore


def get_caption(image: Token) -> str:
    title = image.attrGet("title")
    return title or image.content


def figure(state: StateCore) -> None:
    length = len(state.tokens)

    # do not process first and last token
    for i in range(1, length - 1):
        token = state.tokens[i]

        if token.type != "inline":
            continue

        children_len = len(token.children)

        if not token.children or (children_len != 1 and children_len != 3):
            # children: image alone, or link_open -> image -> link_close
            continue

        if children_len == 1 and token.children[0].type != "image":
            # one child, should be img
            continue

        if children_len == 3:
            # three children, should be image enclosed in link
            [childrenA, childrenB, childrenC] = token.children
            isEnclosed = (
                childrenA.type != "link_open"
                or childrenB.type != "image"
                or childrenC.type != "link_close"
            )

            if isEnclosed:
                continue

        if i != 0 and state.tokens[i - 1].type != "paragraph_open":
            # prev token is paragraph open
            continue

        if i != length - 1 and state.tokens[i + 1].type != "paragraph_close":
            # next token is paragraph close
            continue

        # We have inline token containing an image only.
        # Previous token is paragraph open.
        # Next token is paragraph close.
        # Lets replace the paragraph tokens with figure tokens.
        figure = state.tokens[i - 1]

        figure.type = "figure_open"
        figure.tag = "p"
        figure.attrSet("class", "osu-md__figure-container")

        state.tokens[i + 1].type = "figure_close"
        state.tokens[i + 1].tag = "figure"

        # for linked images, image is one off
        image = token.children[0] if children_len == 1 else token.children[1]

        image.attrSet("class", "osu-md__figure-image")

        fig_caption = get_caption(image)

        if fig_caption == "":
            continue

        openCaption = Token("figcaption_open", "em", 1)
        openCaption.attrSet("class", "osu-md__figure-caption")

        captionText = Token("text", "", 0)
        captionText.content = fig_caption

        closeCaption = Token("figcaption_close", "em", -1)

        token.children.extend([openCaption, captionText, closeCaption])


def figure_plugin(md: MarkdownIt) -> None:
    md.core.ruler.before("linkify", "figure", figure)
