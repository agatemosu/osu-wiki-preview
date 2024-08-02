from bs4 import BeautifulSoup

from plugins.anchors import slugify


def generate_toc(html) -> str:
    soup = BeautifulSoup(html, "html.parser")

    toc = '<ol class="wiki-toc-list wiki-toc-list--top">'
    current_level = 2

    for tag in soup.find_all(["h2", "h3"]):
        text = tag.get_text(strip=True)
        tag_id = tag.get("id") or slugify(text)

        level = int(tag.name[1])

        if level > current_level:
            toc += '<ol class="wiki-toc-list">'
        elif level < current_level:
            toc += "</ol></li>"

        link_class = "wiki-toc-list__link--small" if level == 3 else ""

        toc += f'<li class="wiki-toc-list__item"><a href="#{tag_id}" class="wiki-toc-list__link {link_class}">{text}</a>'

        if level == 3:
            toc += "</li>"

        current_level = level

    toc += "</ol>"
    toc += "</li>" + (current_level - 2) * "</ol>"

    return toc
