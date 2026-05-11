import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
PROBLEMS_DIR = os.path.join(BASE_DIR, "problems")
TEMPLATE_RUST_FILE = os.path.join(BASE_DIR, "templates", "main.rs")
TEMPLATE_PYTHON_FILE = os.path.join(BASE_DIR, "templates", "main.py")
PORT = 10043

# Set to True to use the short problem code (e.g. "p_4a", "p_42") as the
# folder name instead of the full verbose name.  Falls back to the verbose
# name when no code can be extracted.  Defaults to False (verbose name).
USE_PROBLEM_CODE_AS_FOLDER = False
