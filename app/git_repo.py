import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

import humanize
from git import Diff, Repo

from app.meta.config import OSU_WIKI_PATH

repo = Repo(OSU_WIKI_PATH)


class Colour(Enum):
    Blue = "#66ccff"
    Green = "#88b300"
    Red = "#ed1221"
    Yellow = "#ffcc22"


@dataclass
class ChangedFile:
    path: str | None
    colour: Colour
    verb: str
    last_mod: dict[str, str]


def get_display(item: Diff) -> tuple[Colour, str]:
    if item.renamed_file:
        return Colour.Blue, "renamed"

    if item.deleted_file:
        return Colour.Red, "deleted"

    if item.new_file:
        return Colour.Green, "added"

    return Colour.Yellow, "modified"


def get_last_mod(path: str | None, is_deleted: bool = False) -> dict[str, str]:
    if not path:
        return {}

    if is_deleted:
        commit = next(repo.iter_commits(paths=path, max_count=1))
        dt = commit.committed_datetime

    else:
        file_path = os.path.join(OSU_WIKI_PATH, path)

        timestamp = os.path.getmtime(file_path)
        dt = datetime.fromtimestamp(timestamp)

    return {
        "iso": dt.isoformat(timespec="seconds"),
        "ago": humanize.naturaltime(dt),
    }


def get_changed_files() -> list[ChangedFile]:
    changed_files = []

    for file in repo.untracked_files:
        last_mod = get_last_mod(file)
        c_file = ChangedFile(file, Colour.Green, "untracked", last_mod)
        changed_files.append(c_file)

    for item in repo.head.commit.diff(None):
        assert type(item) is Diff
        file_path = (
            f"{item.a_path} → {item.b_path}" if item.renamed_file else item.b_path
        )

        color, verb = get_display(item)
        last_mod = get_last_mod(item.b_path, item.deleted_file)

        c_file = ChangedFile(file_path, color, verb, last_mod)
        changed_files.append(c_file)

    return changed_files


def get_owner_name() -> str:
    remote = repo.remotes[0]

    remote_url = remote.url

    owner = remote_url.split("/")[-2]

    return owner


def get_repo_data() -> dict[str, Any]:
    changed_files = get_changed_files()
    repo_data = {
        "active_branch": repo.active_branch.name,
        "branches": repo.branches,
        "changed_files": changed_files,
        "changed_files_count": len(changed_files),
        "owner": get_owner_name(),
    }

    return repo_data
