from typing import Any, Union

from bs4 import BeautifulSoup, Tag


class TocItem:
    text: str
    id: str

    def __init__(self, tag: Tag) -> None:
        self.text = tag.text
        self.id = tag.attrs["id"]


LevelWithSubItems = tuple[TocItem, list[TocItem]]
Toc = list[TocItem | LevelWithSubItems]


def get_next_el(lst: list, index: int) -> Any | None:
    if index < len(lst) - 1:
        return lst[index + 1]
    else:
        return None


def lvl(tag: Tag) -> int:
    return int(tag.name[1])


def add_item(toc: Toc, el: Tag) -> None:
    if lvl(el) == 2:
        toc.append(TocItem(el))

    if lvl(el) == 3:
        if not isinstance(toc[-1], tuple):
            raise Exception(f"Type of toc item not correct: {type(toc[-1])}")

        toc[-1][1].append(TocItem(el))


def get_toc(html: str) -> Toc:
    soup = BeautifulSoup(html, "html.parser")

    headings = soup.select("h2, h3")
    headings_count = len(headings)

    toc: Toc = []

    for i in range(headings_count):
        curr_el = headings[i]
        next_el = get_next_el(headings, i)

        if i == 0 and lvl(curr_el) == 3:
            raise Exception("Toc cannot start with 3")

        if next_el is None:
            add_item(toc, curr_el)
            break

        if lvl(curr_el) < lvl(next_el):
            toc.append((TocItem(curr_el), []))
            continue

        add_item(toc, curr_el)

    return toc


def ul(classlist: list[str]) -> str:
    classname = " ".join(classlist)
    return f'<ul class="{classname}">'


def link(item: TocItem, classlist: list[str]) -> str:
    classname = " ".join(classlist)
    return f'<a href="#{item.id}" class="{classname}">{item.text}</a>'


def create_toc_html(
    items: Union[Toc, LevelWithSubItems],
    top: bool = True,
) -> str:
    ul_classlist = ["wiki-toc-list"]
    if top:
        ul_classlist.append("wiki-toc-list--top")

    html = ul(ul_classlist)
    for item in items:
        html += '<li class="wiki-toc-list__item">'

        link_classlist = ["wiki-toc-list__link"]
        if not top:
            link_classlist.append("wiki-toc-list__link--small")

        if isinstance(item, TocItem):
            html += link(item, link_classlist)

        elif isinstance(item, tuple):
            main_item, sub_items = item
            html += link(main_item, link_classlist)
            html += create_toc_html(sub_items, False)

        html += "</li>"

    html += "</ul>"
    return html


def generate_toc(html: str) -> str:
    toc = get_toc(html)
    toc_html = create_toc_html(toc)

    return toc_html
