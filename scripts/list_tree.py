import os

from meta.config import OSU_WIKI_PATH


def list_tree(article) -> tuple[list[str], list[str]]:
    article_path = os.path.join(OSU_WIKI_PATH, "wiki", article)

    subdirectories = [
        subdir
        for subdir in os.listdir(article_path)
        if os.path.isdir(os.path.join(article_path, subdir))
    ]

    locales_available = [
        file.replace(".md", "")
        for file in os.listdir(article_path)
        if file.endswith(".md")
    ]

    return subdirectories, locales_available
