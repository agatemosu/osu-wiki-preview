from bs4 import BeautifulSoup


def get_article_title(html: str, article: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for i in range(1, 7):
        tag = soup.find(f"h{i}")

        if tag:
            return tag.text

    return article
