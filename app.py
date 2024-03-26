import os
import subprocess
import webbrowser

import yaml
from bs4 import BeautifulSoup
from flask import Flask, redirect, render_template, request, send_from_directory

from functions.generate_toc import generate_toc
from functions.get_flag_codepoint import get_flag_codepoint
from functions.git import get_branch_name, get_owner_name
from functions.language_list import display_language_list
from functions.list_tree import list_tree
from functions.markdown_converter import convert_to_html, load_front_matter
from functions.process_console_output import process_console_output
from meta.config import HOST, OSU_WIKI_PATH
from meta.languages import locales_dict

app = Flask(__name__)


@app.before_request
def remove_trailing_slash():
    if request.path != "/" and request.path.endswith("/"):
        new_path = request.path[:-1]
        return redirect(new_path)


@app.route("/")
@app.route("/wiki")
def redirect_to_main_page():
    return redirect("/wiki/en/Main_page")


@app.route("/wiki/<path:article>")
@app.route("/wiki/<locale>/<path:article>")
def wiki(article: str, locale: str = ""):
    # Redirect if no locale is specified
    if not locale:
        return redirect(f"/wiki/en/{article}")
    # Redirect if part of the path to the article is taken as locale
    elif locale not in locales_dict:
        return redirect(f"/wiki/en/{locale}/{article}")

    # Redirect old routes
    redirect_file_path = os.path.join(OSU_WIKI_PATH, "wiki", "redirect.yaml")
    with open(redirect_file_path, encoding="utf-8") as redirect_file:
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

    subdirectories, locales_available = list_tree(article)
    language, languages_available, current_flag, available_flags = (
        display_language_list(locale, locales_available)
    )

    with open(article_path, encoding="utf-8") as file:
        markdown_content = file.read()

    html_content = convert_to_html(markdown_content, article, locale)

    # Get the first heading content
    soup = BeautifulSoup(html_content, "html.parser")
    h1_content = soup.find("h1").text

    return render_template(
        "wiki.html",
        content=html_content,
        front_matter=load_front_matter(markdown_content),
        toc=generate_toc(html_content),
        repository_owner=get_owner_name(),
        current_branch=get_branch_name(),
        github_path=wiki_path,
        article_path=article,
        parent_pages=os.path.dirname(article),
        h1_content=h1_content,
        current_locale=locale,
        locales_available=locales_available,
        current_language=language,
        languages_available=languages_available,
        current_flag=current_flag,
        available_flags=available_flags,
    )


@app.route("/wiki/<locale>/Main_page")
def main_page(locale: str, article: str = "Main_page"):
    wiki_path = f"wiki/{article}/{locale}.md"
    article_path = os.path.join(OSU_WIKI_PATH, wiki_path)

    if "open" in request.args:
        webbrowser.open(article_path)
        return redirect(request.path)

    subdirectories, locales_available = list_tree(article)
    language, languages_available, current_flag, available_flags = (
        display_language_list(locale, locales_available)
    )

    with open(article_path, encoding="utf-8") as file:
        markdown_content = file.read()

    html_content = convert_to_html(markdown_content, article, locale)

    return render_template(
        "main-page.html",
        content=html_content,
        front_matter=load_front_matter(markdown_content),
        repository_owner=get_owner_name(),
        current_branch=get_branch_name(),
        github_path=wiki_path,
        current_locale=locale,
        locales_available=locales_available,
        current_language=language,
        languages_available=languages_available,
        current_flag=current_flag,
        available_flags=available_flags,
    )


@app.route("/osu-wiki-tools/wiki/<path:article>/<locale>.md")
def osu_wiki_tools(article: str, locale: str):
    article_dir = f"wiki/{article}/{locale}.md"

    if "open" in request.args:
        file_path = os.path.join(OSU_WIKI_PATH, article_dir)
        webbrowser.open(file_path)
        return redirect(request.path)

    args = {
        "links": ["osu-wiki-tools", "check-links", "--target", article_dir],
        "yaml": ["osu-wiki-tools", "check-yaml", "--target", article_dir],
    }

    try:
        actual_directory = os.getcwd()
        os.chdir(OSU_WIKI_PATH)

        links = subprocess.run(args["links"], stdout=subprocess.PIPE, text=True)
        yaml = subprocess.run(args["yaml"], stdout=subprocess.PIPE, text=True)

        results = {
            "links": process_console_output(links.stdout),
            "yaml": process_console_output(yaml.stdout),
        }

    except Exception as e:
        results = {"exception": f"Error at running the check: {str(e)}"}

    finally:
        os.chdir(actual_directory)

    language = locales_dict.get(locale, {}).get("name", locale)
    flag = locales_dict.get(locale, {}).get("flag", "fallback")

    return render_template(
        "osu-wiki-tools.html",
        repository_owner=get_owner_name(),
        current_branch=get_branch_name(),
        article_path=article,
        results=results,
        current_locale=locale,
        current_language=language,
        current_flag=flag,
    )


@app.route("/assets/images/flags/<filename>.svg")
def serve_flag(filename: str):
    code = get_flag_codepoint(filename)
    flags_path = "node_modules/@discordapp/twemoji/dist/svg"
    file_path = f"{flags_path}/{code}.svg"

    if os.path.isfile(file_path):
        return send_from_directory(flags_path, f"{code}.svg")
    else:
        return send_from_directory("resources/flags", "fallback.svg")


if __name__ == "__main__":
    app.run(debug=True, host=HOST)
