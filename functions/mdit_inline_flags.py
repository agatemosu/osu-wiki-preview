from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline


def flag_plugin(md: MarkdownIt):
    # Add a rule to the parser to match the custom syntax
    md.inline.ruler.before("text", "flag", parse_flag)


def parse_flag(state: StateInline, silent: bool):
    # Check if the current position has "::{ flag=" at the beginning
    if state.src.startswith("::{ flag=", state.pos):
        # Find the closing "}::"
        end = state.src.find(" }::", state.pos + 9)

        if end != -1:
            # Extract the flag value
            flag_value = state.src[state.pos + 9 : end]

            # Add a token for the custom syntax
            state.push("flag_open", "span", 1).attrs = {
                "class": "flag-country flag-country--flat flag-country--wiki",
                "style": f"background-image: url('/assets/images/flags/{flag_value}.svg');",
            }
            state.push("flag_close", "span", -1)
            state.pos = end + 4

            return True

    return False
