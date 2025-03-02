# osu! wiki preview

## Requirements

### 1. Repositories

_If you don't have a fork of the [osu! wiki](https://github.com/ppy/osu-wiki) repository yet, follow [osu! wiki contribution guide § Editing the wiki](https://osu.ppy.sh/wiki/en/osu!_wiki/Contribution_guide#editing-the-wiki) to set up your fork._

Clone the required repositories using the following commands, replacing `<your-username>` with your GitHub username:

```bash
git clone https://github.com/<your-username>/osu-wiki
git clone https://github.com/ppy/osu-web
git clone https://github.com/agatemosu/osu-wiki-preview
```

The folder structure should look like the following:

```bash
folder/
├───── osu-web/
├───── osu-wiki/
└───── osu-wiki-preview/
```

### 2. Dependencies

1. [uv](https://docs.astral.sh/uv/)
2. [yarn](https://yarnpkg.com/getting-started/install)

To install the dependencies:

```bash
uv sync
yarn install
```

And finally, you will need to build osu!'s CSS with:

```bash
yarn run build
```

## Running the website

Execute the following command to run the website:

```bash
uv run quart run
```

Open your web browser and navigate to <http://localhost:5000/> to access the osu! wiki preview.
