from quart import Quart, redirect, request
import json

from app.routes import assets, wiki, wiki_tools
from app.git_repo import get_repo_data

app = Quart(__name__)
app.register_blueprint(assets.bp)
app.register_blueprint(wiki.bp)
app.register_blueprint(wiki_tools.bp)


@app.context_processor
def inject_globals():
    with open("./app/static/manifest.json") as f:
        manifest = json.load(f)

    return {
        "manifest": manifest,
        "repo_data": get_repo_data(),
    }


@app.before_request
async def remove_trailing_slash():
    if request.path != "/" and request.path.endswith("/"):
        new_path = request.path.rstrip("/")
        return redirect(new_path)


@app.route("/")
@app.route("/wiki")
async def redirect_to_main_page():
    return redirect("/wiki/en/Main_page")
