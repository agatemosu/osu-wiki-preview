import os

from quart import Quart, redirect, request, send_from_directory

from meta.config import HOST
from routes import wiki, wiki_tools

app = Quart(__name__)
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


@app.route("/assets/images/flags/<code>.svg")
async def serve_flag(code: str):
    flags_dir = "node_modules/@discordapp/twemoji/dist/svg"
    target_flag_file = f"{code}.svg"

    if os.path.isfile(f"{flags_dir}/{target_flag_file}"):
        flag_dir = flags_dir
        flag_file = target_flag_file
    else:
        flag_dir = "resources/flags"
        flag_file = "fallback.svg"

    return await send_from_directory(flag_dir, flag_file)


if __name__ == "__main__":
    app.run(debug=True, host=HOST)
