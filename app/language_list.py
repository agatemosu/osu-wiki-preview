from app.get_flag_codepoint import get_flag_codepoint
from meta.languages import locales_dict


def get_lang_info(locale: str) -> dict[str, str]:
    info = locales_dict.get(locale, {"name": locale, "flag": "fallback"})
    language = info["name"]
    flag = get_flag_codepoint(info["flag"])

    return {"name": language, "locale": locale, "flag": flag}


def get_lang_list(locales_available) -> list[dict[str, str]]:
    available_langs = [get_lang_info(code) for code in locales_available]

    return available_langs
