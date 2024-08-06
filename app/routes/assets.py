import os

from quart import Blueprint, send_from_directory

bp = Blueprint("assets", __name__, url_prefix="/assets")


@bp.route("/images/flags/<code>.svg")
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
