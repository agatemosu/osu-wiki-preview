def process_console_output(output: str) -> str:
    color_mapping = {
        "\x1b[0m": "</span>",
        "\x1b[2m": '<span style="color: darkgray">',
        "\x1b[4m": '<span style="color: white">',
        "\x1b[31m": '<span style="color: red">',
        "\x1b[32m": '<span style="color: green">',
        "\x1b[33m": '<span style="color: yellow">',
        "\x1b[34m": '<span style="color: blue">',
        "\x1b[90m": '<span style="color: gray">',
    }

    for code, style in color_mapping.items():
        output = output.replace(code, style).strip()

    return output
