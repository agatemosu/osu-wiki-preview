from git import Repo

from app.meta.config import OSU_WIKI_PATH

repo = Repo(OSU_WIKI_PATH)


def get_branch_name() -> str:
    return repo.active_branch.name


def get_owner_name() -> str:
    remote = repo.remotes[0]

    remote_url = remote.url

    owner = remote_url.split("/")[-2]

    return owner


repo_data = {"branch": get_branch_name(), "owner": get_owner_name()}
