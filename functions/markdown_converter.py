import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins import attrs, container, footnote, front_matter

from functions.html_add_figure_caption import add_figure_caption
from functions.html_modify_content import modify_html_content
from functions.mdit_anchors import anchors_plugin, slugify
from functions.mdit_inline_flags import flag_plugin
from functions.mdit_token_classes import tag_class_plugin


def render_custom(self, tokens: list[Token], idx: int, _options, env):
    if tokens[idx].nesting == 1:
        tokens[idx].attrJoin("class", "osu-md__infobox")

    return self.renderToken(tokens, idx, _options, env)


md = MarkdownIt("commonmark")
md.enable("table")
md.use(front_matter.front_matter_plugin)
md.use(footnote.footnote_plugin)
# Copied because official plugin puts "-" instead of "." if the header repeats
# and attrs plugin does not work with custom identifiers
md.use(anchors_plugin, 2, 5, slugify)
md.use(container.container_plugin, "Infobox", render=render_custom)
# https://osu.ppy.sh/wiki/en/Article_styling_criteria/Formatting#custom-identifiers
# But it only works if {id=identifier} is before
md.use(attrs.attrs_block_plugin)
md.use(flag_plugin)
md.use(
    tag_class_plugin,
    {
        "h1": ["osu-md__header", "osu-md__header--1"],
        "h2": ["osu-md__header", "osu-md__header--2"],
        "h3": ["osu-md__header", "osu-md__header--3"],
        "h4": ["osu-md__header", "osu-md__header--4"],
        "h5": ["osu-md__header", "osu-md__header--5"],
        "h6": ["osu-md__header", "osu-md__header--6"],
        "td": ["osu-md__table-data"],
        "th": ["osu-md__table-data", "osu-md__table-data--header"],
        "ul": ["osu-md__list"],
        "ol": ["osu-md__list-ordened"],
        "a": ["osu-md__link"],
    },
)


def load_front_matter(markdown_content):
    result = md.parse(markdown_content)

    front_matter_tokens = [token for token in result if token.type == "front_matter"]

    if front_matter_tokens:
        front_matter_content = front_matter_tokens[0].content
        front_matter = yaml.safe_load(front_matter_content)

        return front_matter


def convert_to_html(markdown_content, article, locale):
    html_content = md.render(markdown_content)

    if article != "Main_page":
        html_content = modify_html_content(html_content, article, locale)
        html_content = add_figure_caption(html_content)

    return html_content
