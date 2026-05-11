import json
import os
import re
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROBLEMS_DIR = os.path.join(BASE_DIR, "problems")
TEMPLATE_FILE = os.path.join(BASE_DIR, "templates", "main.rs")


def safe_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def create_rust_project(path: str, problem_name: str):
    os.makedirs(os.path.join(path, "src"), exist_ok=True)

    # Cargo.toml
    cargo_toml = f"""
[package]
name = "{problem_name}"
version = "0.1.0"
edition = "2021"
"""

    with open(os.path.join(path, "Cargo.toml"), "w") as f:
        f.write(cargo_toml.strip())

    # main.rs from template
    if os.path.exists(TEMPLATE_FILE):
        shutil.copy(TEMPLATE_FILE, os.path.join(path, "src", "main.rs"))
    else:
        with open(os.path.join(path, "src", "main.rs"), "w") as f:
            f.write('fn main() { println!("Hello"); }')


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length)
        problem = json.loads(data.decode())

        contest = problem.get("contest", "")
        index = problem.get("index", "").lower()
        name = problem.get("name", "").lower()

        folder = f"{contest}_{index}_{re.sub(r'[^a-z0-9]+', '_', name)}"
        folder = re.sub(r"_+", "_", folder).strip("_")

        path = os.path.join(PROBLEMS_DIR, folder)

        os.makedirs(path, exist_ok=True)

        # Create Rust project
        create_rust_project(path, folder)

        # Save samples
        tests = problem.get("tests", [])
        input_file = os.path.join(path, "input.txt")

        with open(input_file, "w", encoding="utf-8") as f:
            for i, test in enumerate(tests):
                f.write(f"--- sample {i + 1} ---\n")
                f.write(test.get("input", ""))
                f.write("\n")

        # Save metadata
        with open(os.path.join(path, "meta.json"), "w", encoding="utf-8") as f:
            json.dump(problem, f, indent=2)

        print(f"[✓] Created Rust project: {name}")
        print(f"[✓] Path: {path}")

        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 10043), Handler)
    print("Listening on http://127.0.0.1:10043")
    server.serve_forever()
