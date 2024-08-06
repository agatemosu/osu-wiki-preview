import os
import webbrowser

from quart import Blueprint, redirect, render_template, request

from app.git_repo import repo_data
from app.language_list import get_lang_info
from app.meta.config import OSU_WIKI_PATH
from app.run_checks import run_checks

bp = Blueprint("osu-wiki-tools", __name__, url_prefix="/osu-wiki-tools")


@bp.route("/wiki/<path:article>/<locale>.md")
async def osu_wiki_tools(article: str, locale: str):
    relative_wiki_path = f"wiki/{article}/{locale}.md"

    if "open" in request.args:
        absolute_file_path = os.path.join(OSU_WIKI_PATH, relative_wiki_path)
        webbrowser.open(absolute_file_path)
        return redirect(request.path)

    results = run_checks(relative_wiki_path)
    current_lang = get_lang_info(locale)

    return await render_template(
        "osu-wiki-tools.jinja",
        relative_wiki_path=relative_wiki_path,
        article=article,
        results=results,
        current_lang=current_lang,
        header_items=[
            {"name": "osu-wiki-tools"},
            {"name": relative_wiki_path},
        ],
        repo_data=repo_data,
    )
