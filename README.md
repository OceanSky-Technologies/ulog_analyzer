# ulog_analyzer

This repo provides tooling to visualize and analyze ulog files.

Ulog is the default log file format used by PX4. For infos see [this page](https://docs.px4.io/main/en/dev_log/ulog_file_format.html).

## Usage

Set up a virtual environment and enter it:

```bash
python3 -m venv ./.venv

# Linux
source ./venv/bin/.activate

# Windows
.\.venv\Scripts\activate
```

Install necessary libraries inside this venv:

```bash
python3 -m pip install -r requirements.txt
```

Run the analyzer script with

```bash
python3 .\analyze.py PATH_TO_ULG_FILE
```

Then open the URL `http://127.0.0.1:8050/` in a browser.

If you require more python packages inside this venv, you can add them using `pip3 install ...` and save them to the venv using

```bash
pip3 freeze > requirements.txt
``````

You can leave the venv any time using

```bash
deactivate
```

In `vscode` you can create or use the existing venv with `Ctrl+Shift+P` -> `Python: Create Environment`.
