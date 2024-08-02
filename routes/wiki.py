import os
import webbrowser

import yaml
from bs4 import BeautifulSoup
from flask import (
    Blueprint,
    Response,
    redirect,
    render_template,
    request,
    send_from_directory,
)

from meta.config import OSU_WIKI_PATH, REDIRECT_FILE_PATH
from meta.languages import locales_dict
from scripts.generate_toc import generate_toc
from scripts.git import get_branch_name, get_owner_name
from scripts.language_list import get_lang_info, get_lang_list
from scripts.list_tree import list_tree
from scripts.markdown_converter import convert_to_html, load_front_matter

bp = Blueprint("wiki", __name__, url_prefix="/wiki")


@bp.route("/<path:article>")
@bp.route("/<locale>/<path:article>")
def wiki(article: str, locale: str = "") -> Response | str:
    # Redirect if no locale is specified
    if not locale:
        return redirect(f"/wiki/en/{article}")
    # Redirect if part of the path to the article is taken as locale
    elif locale not in locales_dict:
        return redirect(f"/wiki/en/{locale}/{article}")

    # Redirect old routes
    with open(REDIRECT_FILE_PATH, encoding="utf-8") as redirect_file:
        redirect_mappings = yaml.safe_load(redirect_file)

    if article.lower() in redirect_mappings:
        new_path = redirect_mappings[article.lower()]
        return redirect(f"/wiki/{locale}/{new_path}")

    # Serve images as static image files
    if article.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg")):
        file_name = os.path.basename(article)
        img_path = os.path.join(OSU_WIKI_PATH, "wiki", os.path.dirname(article))

        return send_from_directory(img_path, file_name)

    # Get the link for GitHub and the article path in this computer
    wiki_path = f"wiki/{article}/{locale}.md"
    article_path = os.path.join(OSU_WIKI_PATH, wiki_path)

    if "open" in request.args:
        webbrowser.open(article_path)
        return redirect(request.path)

    _, locales_available = list_tree(article)
    current_lang = get_lang_info(locale)
    available_langs = get_lang_list(locales_available)

    with open(article_path, encoding="utf-8") as file:
        markdown_content = file.read()

    html_content = convert_to_html(markdown_content, article, locale)

    # Get the first heading content
    soup = BeautifulSoup(html_content, "html.parser")
    h1_content = soup.find("h1").text

    parent_pages = os.path.dirname(article)
    header_items = [
        {"name": "index", "href": f"/wiki/{locale}/Main_page"},
        {"name": h1_content, "href": f"/wiki/{locale}/{article_path}"},
    ]

    if parent_pages:
        header_items.insert(
            1,
            {"name": parent_pages, "href": f"/wiki/{locale}/{parent_pages}"},
        )

    return render_template(
        "wiki.jinja",
        content=html_content,
        front_matter=load_front_matter(markdown_content),
        toc=generate_toc(html_content),
        repository_owner=get_owner_name(),
        current_branch=get_branch_name(),
        wiki_path=wiki_path,
        article_path=article,
        h1_content=h1_content,
        current_lang=current_lang,
        available_langs=available_langs,
        header_items=header_items,
    )


@bp.route("/<locale>/Main_page")
def main_page(locale: str, article: str = "Main_page") -> Response | str:
    wiki_path = f"wiki/{article}/{locale}.md"
    article_path = os.path.join(OSU_WIKI_PATH, wiki_path)

    if "open" in request.args:
        webbrowser.open(article_path)
        return redirect(request.path)

    _, locales_available = list_tree(article)
    current_lang = get_lang_info(locale)
    available_langs = get_lang_list(locales_available)

    with open(article_path, encoding="utf-8") as file:
        markdown_content = file.read()

    html_content = convert_to_html(markdown_content, article, locale)

    return render_template(
        "main-page.jinja",
        content=html_content,
        front_matter=load_front_matter(markdown_content),
        repository_owner=get_owner_name(),
        wiki_path=wiki_path,
        current_lang=current_lang,
        available_langs=available_langs,
        header_items=[{"name": f"index (on branch <b>{get_branch_name()}</b>)"}],
    )
