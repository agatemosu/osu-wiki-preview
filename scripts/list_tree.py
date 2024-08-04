import os

from meta.config import OSU_WIKI_PATH
from meta.languages import locales_dict


def get_available_locales(article) -> list[str]:
    article_path = os.path.join(OSU_WIKI_PATH, "wiki", article)

    available_locales = [
        locale
        for file in os.listdir(article_path)
        if file.endswith(".md")
        and (path := os.path.join(article_path, file))
        and os.path.isfile(path)
        and (locale := file[:-3])
        and locale in locales_dict
    ]

    return available_locales
