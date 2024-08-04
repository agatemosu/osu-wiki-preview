import os

from meta.config import OSU_WIKI_PATH
from meta.languages import locales_dict


def list_tree(article) -> tuple[list[str], list[str]]:
    article_path = os.path.join(OSU_WIKI_PATH, "wiki", article)

    subdirectories = [
        subdir
        for subdir in os.listdir(article_path)
        if os.path.isdir(os.path.join(article_path, subdir))
    ]

    locales_available = [
        locale
        for file in os.listdir(article_path)
        if file.endswith(".md")
        and (path := os.path.join(article_path, file))
        and os.path.isfile(path)
        and (locale := file[:-3])
        and locale in locales_dict
    ]

    return subdirectories, locales_available
