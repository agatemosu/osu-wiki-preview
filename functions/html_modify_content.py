import re

from bs4 import BeautifulSoup


def modify_html_content(html, article, locale):
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

    # Fix tables overflowing
    for table in soup.find_all("table"):
        table.wrap(soup.new_tag("div", attrs={"class": "osu-md__table"}))

    # Add divs to wrap the content of the lists
    # (because osu-web's CSS is broken with lists)
    for li in soup.find_all("li"):
        div = soup.new_tag("div")
        while li.contents:
            div.append(li.contents[0])
        li.append(div)

    # Add figure classes
    for p in soup.find_all("p"):
        if p.find("img"):
            p["class"] = "osu-md__figure-container"
            for img in p.find_all("img"):
                img["class"] = "osu-md__figure-image"
        else:
            p["class"] = "osu-md__paragraph"

    # Change the ref symbol to be the same as osu-web
    for ref in soup.find_all(class_="footnote-backref"):
        ref.string = "↑"

    return str(soup)
