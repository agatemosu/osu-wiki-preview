from meta.languages import locales_dict


def display_language_list(current_locale, locales_available):
    language = locales_dict.get(current_locale, {}).get("name", current_locale)
    languages_available = [
        locales_dict.get(code, {}).get("name", code) for code in locales_available
    ]

    current_flag = locales_dict.get(current_locale, {}).get("flag", "fallback")
    available_flags = [
        locales_dict.get(code, {}).get("flag", "fallback") for code in locales_available
    ]

    return language, languages_available, current_flag, available_flags
