import subprocess

from app.meta.config import OSU_WIKI_PATH
from app.process_console_output import process_console_output


def run_checks(relative_wiki_path: str) -> list[str]:
    params = [
        ["osu-wiki-tools", "check-links", "--target", relative_wiki_path],
        ["osu-wiki-tools", "check-yaml", "--target", relative_wiki_path],
    ]

    try:
        results = []
        for param in params:
            result = subprocess.run(
                param, stdout=subprocess.PIPE, cwd=OSU_WIKI_PATH, text=True
            )
            results.append(process_console_output(result.stdout))

    except Exception as e:
        results = [f"Error at running the check: {str(e)}"]

    return results
