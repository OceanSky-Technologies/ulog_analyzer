# ulog_analyzer

This repo provides additional tooling to visualize and analyze ulog files that extends https://logs.px4.io/.

Ulog is the log file format used by PX4. For infos see [this page](https://docs.px4.io/main/en/dev_log/ulog_file_format.html).

## Usage

Set up a virtual environment and enter it:

```bash
python -m venv ./.venv

# Linux
source ./.venv/bin/activate

# Windows
# first allow virtual environments: start a terminal with admin permissions and run
Set-ExecutionPolicy Unrestricted -Force

# afterwards you can launch the venv with
.\.venv\Scripts\activate
```

Install necessary libraries inside this venv:

```bash
python -m pip install -r requirements.txt
```

Run the analyzer script with

```bash
python ./analyze.py PATH_TO_ULG_FILE
```

Then open the URL `http://127.0.0.1:8050/` in a browser.

If you require more python packages inside this venv, you can add them using `pip install ...` and save them to the venv using

```bash
pip freeze > requirements.txt
``````

You can leave the venv any time using

```bash
deactivate
```

In `vscode` you can create or use the existing venv with `Ctrl+Shift+P` -> `Python: Create Environment`.
