import os

from flask import Flask, Response, redirect, request, send_from_directory

from meta.config import HOST
from routes import wiki, wiki_tools

app = Flask(__name__)
app.register_blueprint(wiki.bp)
app.register_blueprint(wiki_tools.bp)


@app.before_request
def remove_trailing_slash() -> Response | None:
    if request.path != "/" and request.path.endswith("/"):
        new_path = request.path.rstrip("/")
        return redirect(new_path)


@app.route("/")
@app.route("/wiki")
def redirect_to_main_page() -> Response:
    return redirect("/wiki/en/Main_page")


@app.route("/assets/images/flags/<code>.svg")
def serve_flag(code: str) -> Response:
    flags_dir = "node_modules/@discordapp/twemoji/dist/svg"
    target_flag_file = f"{code}.svg"

    if os.path.isfile(f"{flags_dir}/{target_flag_file}"):
        flag_dir = flags_dir
        flag_file = target_flag_file
    else:
        flag_dir = "resources/flags"
        flag_file = "fallback.svg"

    return send_from_directory(flag_dir, flag_file, max_age=3600)


if __name__ == "__main__":
    app.run(debug=True, host=HOST)
