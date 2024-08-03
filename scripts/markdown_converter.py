import io
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from mdit_py_plugins import attrs, container, footnote, front_matter
from wikitools import article_parser

from plugins import anchors, figure, flag, osu_footnote, osu_list
from scripts.html_modify_content import modify_html_content


class OsuRenderer(RendererHTML):
    def list_item_open(self, tokens, idx, options, env):
        return "<li><div>"

    def list_item_close(self, tokens, idx, options, env):
        return "</div></li>"

    def table_open(self, tokens, idx, options, env):
        return '<div class="osu-md__table"><table>'

    def table_close(self, tokens, idx, options, env):
        return "</table></div>"


md = MarkdownIt("commonmark", renderer_cls=OsuRenderer)
md.enable("table")

md.use(front_matter.front_matter_plugin)

md.use(container.container_plugin, "Infobox")
md.use(figure.figure_plugin)

md.use(footnote.footnote_plugin)
md.use(osu_footnote.footnote_plugin)

md.use(osu_list.osu_list_plugin)

md.use(flag.flag_plugin)

# https://osu.ppy.sh/wiki/en/Article_styling_criteria/Formatting#custom-identifiers
# But it only works if {id=identifier} is before
md.use(attrs.attrs_block_plugin)

# Copied because official plugin puts "-" instead of "." if the header repeats
# and attrs plugin does not work with custom identifiers
md.use(anchors.anchors_plugin, 2, 5)


def load_front_matter(markdown_content: str) -> dict[str, Any]:
    return article_parser.load_front_matter(io.StringIO(markdown_content))


def convert_to_html(markdown_content: str, article: str, locale: str) -> str:
    html_content = md.render(markdown_content)

    html_content = modify_html_content(html_content, article, locale)

    return html_content
