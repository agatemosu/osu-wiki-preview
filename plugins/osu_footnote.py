from typing import Sequence

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict


def getFootnoteId(tokens: Sequence[Token], idx: int) -> int:
    return tokens[idx].meta["id"] + 1


def getFootnoteRefId(tokens: Sequence[Token], idx: int, id: int) -> str:
    return f'fnref-{id}__{tokens[idx].meta["subId"]}'


def render_footnote_ref(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    id = getFootnoteId(tokens, idx)
    refid = getFootnoteRefId(tokens, idx, id)
    return f'<sup id="{refid}"><a href="#fn-{id}" class="osu-md__link--footnote-ref">{id}</a></sup>'


def render_footnote_block_open(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    return '<section class="osu-md__footnote-container"><ol>'


def render_footnote_open(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    id = getFootnoteId(tokens, idx)
    return f'<li id="fn-{id}" class="osu-md__list-item--footnote">'


def render_footnote_anchor(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    id = getFootnoteId(tokens, idx)
    refid = getFootnoteRefId(tokens, idx, id)
    return f'&nbsp;<a href="#{refid}">↑</a>'


def footnote_plugin(md: MarkdownIt) -> None:
    md.add_render_rule("footnote_ref", render_footnote_ref)
    md.add_render_rule("footnote_block_open", render_footnote_block_open)
    md.add_render_rule("footnote_open", render_footnote_open)
    md.add_render_rule("footnote_anchor", render_footnote_anchor)
