import re

from bs4 import BeautifulSoup


def modify_html_content(html: str, article: str, locale: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Fix wikilinks
    for tag in soup.find_all(["a", "img"]):
        if "href" in tag.attrs:
            href = tag["href"]

            # Skip links that start with "#", "http://", "https://", "mailto:"
            if re.match(r"^(#|https?://|mailto:)", href):
                continue

            elif re.match(r"^(\.|[A-Za-z0-9])", href):
                tag["href"] = f"/wiki/{locale}/{article}/{href}"

            elif href.startswith("/wiki/"):
                tag["href"] = f"/wiki/{locale}/{href[6:]}"

        elif "src" in tag.attrs and tag["src"].startswith("img/"):
            tag["src"] = f"/wiki/{article}/{tag['src']}"

    return str(soup)
