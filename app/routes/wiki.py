import os
import webbrowser

import yaml
from quart import Blueprint, redirect, render_template, request, send_from_directory

from app.get_article_title import get_article_title
from app.git_repo import repo_data
from app.language_list import get_lang_info, get_lang_list
from app.list_tree import get_available_locales
from app.markdown_converter import convert_to_html, load_front_matter
from app.meta.config import OSU_WIKI_PATH, REDIRECT_FILE_PATH
from app.meta.languages import locales_dict
from app.toc import generate_toc

bp = Blueprint("wiki", __name__, url_prefix="/wiki")


async def serve_image(res: str, article: str):
    if res in locales_dict:
        return redirect(f"/wiki/{article}")

    absolute_img_path = os.path.join(OSU_WIKI_PATH, "wiki", res, article)

    img_dir = os.path.dirname(absolute_img_path)
    img_filename = os.path.basename(absolute_img_path)

    return await send_from_directory(img_dir, img_filename)


@bp.route("/<res>")
def redirect_missing_paths(res: str):
    if res in locales_dict:
        return redirect(f"/wiki/{res}/Main_page")

    return redirect(f"/wiki/en/{res}")


@bp.route("/<locale>/<path:article>")
async def wiki(locale: str, article: str):
    # Serve images as static image files
    if article.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg")):
        return await serve_image(locale, article)

    # Redirect if part of the path to the article is taken as locale
    if locale not in locales_dict:
        return redirect(f"/wiki/en/{locale}/{article}")

    # Redirect old routes
    with open(REDIRECT_FILE_PATH, encoding="utf-8") as redirect_file:
        redirect_mappings = yaml.safe_load(redirect_file)

    if article.lower() in redirect_mappings:
        new_path = redirect_mappings[article.lower()]
        return redirect(f"/wiki/{locale}/{new_path}")

    # Get the link for GitHub and the article path in this computer
    relative_wiki_path = f"wiki/{article}/{locale}.md"
    absolute_article_path = os.path.join(OSU_WIKI_PATH, relative_wiki_path)

    current_lang = get_lang_info(locale)
    header_items = [{"name": "index", "href": f"/wiki/{locale}/Main_page"}]

    if not os.path.isfile(absolute_article_path):
        header_items.append({"name": "Not found"})

        return await render_template(
            "not-found.jinja",
            article_path=article,
            relative_wiki_path=relative_wiki_path,
            current_lang=current_lang,
            header_items=header_items,
            repo_data=repo_data,
        )

    if "open" in request.args:
        webbrowser.open(absolute_article_path)
        return redirect(request.path)

    with open(absolute_article_path, encoding="utf-8") as file:
        markdown_content = file.read()

    available_locales = get_available_locales(article)
    available_langs = get_lang_list(available_locales)

    front_matter = load_front_matter(markdown_content)
    html_content = convert_to_html(markdown_content, article, locale)

    if front_matter.get("layout") == "main_page":
        header_items.append({"name": repo_data["branch"]})

        return await render_template(
            "main-page.jinja",
            html_content=html_content,
            front_matter=front_matter,
            article_path=article,
            relative_wiki_path=relative_wiki_path,
            current_lang=current_lang,
            available_langs=available_langs,
            header_items=header_items,
            repo_data=repo_data,
        )

    # Get the first heading content
    article_title = get_article_title(html_content, article)
    toc = generate_toc(html_content)

    parent_pages = os.path.dirname(article)
    if parent_pages:
        last_parent = parent_pages.split("/")[-1]

        header_items.append(
            {
                "name": last_parent.replace("_", " "),
                "href": f"/wiki/{locale}/{parent_pages}",
            },
        )

    header_items.append(
        {"name": article_title, "href": f"/wiki/{locale}/{article}"},
    )

    return await render_template(
        "wiki.jinja",
        html_content=html_content,
        front_matter=front_matter,
        article_title=article_title,
        article_path=article,
        toc=toc,
        relative_wiki_path=relative_wiki_path,
        current_lang=current_lang,
        available_langs=available_langs,
        repo_data=repo_data,
        header_items=header_items,
    )
