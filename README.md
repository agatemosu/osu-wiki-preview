# osu! wiki preview

## Requirements

### 1. The repository

_If you don't have a fork of the [osu! wiki](https://github.com/ppy/osu-wiki) repository yet, follow [osu! wiki contribution guide § Editing the wiki](https://osu.ppy.sh/wiki/en/osu!_wiki/Contribution_guide#editing-the-wiki) to set up your fork._

Clone the osu! wiki repository using the following command, replacing `<your-username>` with your GitHub username:

```bash
git clone https://github.com/<your-username>/osu-wiki
```

To clone the osu! wiki preview repository, run the following command in the same folder as `osu-wiki`:

```bash
git clone https://github.com/agatemosu/osu-wiki-preview
```

Additionally, you will also need osu!web:

```bash
git clone https://github.com/ppy/osu-web
```

The folder structure should look like the following:

```bash
folder/
├───── osu-web/
├───── osu-wiki/
└───── osu-wiki-preview/
```

### 2. Dependencies

#### pip

Create a virtual environment with:

```bash
python -m venv venv
```

And activate it with [the corresponding command](https://docs.python.org/3/library/venv.html#how-venvs-work).

Then, install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

#### yarn

Install yarn and npm dependencies:

```bash
npm -g yarn
yarn install
```

You'll need to build osu!'s CSS with:

```bash
yarn run build
```

## Running the website

Execute the following command to run the website:

```bash
flask run
```

Open your web browser and navigate to <http://localhost:5000/> to access the osu! wiki preview.
