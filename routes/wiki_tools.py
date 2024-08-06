import os
import webbrowser

from quart import Blueprint, redirect, render_template, request

from meta.config import OSU_WIKI_PATH
from scripts.git_repo import get_branch_name, get_owner_name
from scripts.language_list import get_lang_info
from scripts.run_checks import run_checks

bp = Blueprint("osu-wiki-tools", __name__, url_prefix="/osu-wiki-tools")


@bp.route("/wiki/<path:article>/<locale>.md")
async def osu_wiki_tools(article: str, locale: str):
    wiki_path = f"wiki/{article}/{locale}.md"

    if "open" in request.args:
        file_path = os.path.join(OSU_WIKI_PATH, wiki_path)
        webbrowser.open(file_path)
        return redirect(request.path)

    results = run_checks(wiki_path)
    current_lang = get_lang_info(locale)

    return await render_template(
        "osu-wiki-tools.jinja",
        repository_owner=get_owner_name(),
        current_branch=get_branch_name(),
        wiki_path=wiki_path,
        article_path=article,
        results=results,
        current_lang=current_lang,
        header_items=[
            {"name": "osu-wiki-tools"},
            {"name": wiki_path},
        ],
    )
