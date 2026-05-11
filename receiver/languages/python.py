import os
import shutil

from config import TEMPLATE_PYTHON_FILE

SUBDIR = "python"


def create_project(path: str, folder: str):
    src_dir = os.path.join(path, "src")
    os.makedirs(src_dir, exist_ok=True)

    if os.path.exists(TEMPLATE_PYTHON_FILE):
        shutil.copy(TEMPLATE_PYTHON_FILE, os.path.join(src_dir, "main.py"))
    else:
        with open(os.path.join(src_dir, "main.py"), "w") as f:
            f.write("import sys\ninput = sys.stdin.readline\n\n\ndef main():\n    pass\n\n\nif __name__ == \"__main__\":\n    main()\n")


def readme_commands(folder: str) -> list:
    return [
        "## Run",
        "",
        "### From repo root:",
        "```bash",
        f"python problems/python/{folder}/src/main.py < problems/python/{folder}/tests/1.in",
        "```",
        "",
        "### Diff against expected output:",
        "```bash",
        f"python problems/python/{folder}/src/main.py < problems/python/{folder}/tests/1.in | diff - problems/python/{folder}/tests/1.out",
        "```",
    ]
