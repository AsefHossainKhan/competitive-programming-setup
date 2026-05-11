import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
PROBLEMS_DIR = os.path.join(BASE_DIR, "problems")
TEMPLATE_RUST_FILE = os.path.join(BASE_DIR, "templates", "main.rs")
TEMPLATE_PYTHON_FILE = os.path.join(BASE_DIR, "templates", "main.py")
PORT = 10043
