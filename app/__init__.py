from quart import Quart, redirect, request

from app.routes import assets, wiki, wiki_tools

app = Quart(__name__)
app.register_blueprint(assets.bp)
app.register_blueprint(wiki.bp)
app.register_blueprint(wiki_tools.bp)


@app.before_request
async def remove_trailing_slash():
    if request.path != "/" and request.path.endswith("/"):
        new_path = request.path.rstrip("/")
        return redirect(new_path)


@app.route("/")
@app.route("/wiki")
async def redirect_to_main_page():
    return redirect("/wiki/en/Main_page")
