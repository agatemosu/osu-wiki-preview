import os

from quart import Blueprint, send_from_directory

bp = Blueprint("assets", __name__, url_prefix="/assets")


@bp.route("/images/flags/<code>.svg")
async def serve_flag(code: str):
    flag_dir = "node_modules/@discordapp/twemoji/dist/svg"
    flag_file = f"{code}.svg"

    if not os.path.isfile(f"{flag_dir}/{flag_file}"):
        flag_dir = "resources/flags"
        flag_file = "fallback.svg"

    return await send_from_directory(flag_dir, flag_file)
