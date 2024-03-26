def get_flag_codepoint(code: str) -> str:
    if len(code) != 2:
        return "1f1fd-1f1fd"

    regional_indicator_a = ord(code[0].upper()) + 127397  # Offset between the letters
    regional_indicator_b = ord(code[1].upper()) + 127397  # and the regional indicators

    return f"{regional_indicator_a:04x}-{regional_indicator_b:04x}"
