import json
import os
import re
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer

# Always resolve paths relative to this script file, regardless of CWD.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
PROBLEMS_DIR = os.path.join(BASE_DIR, "problems")
TEMPLATE_FILE = os.path.join(BASE_DIR, "templates", "main.rs")


def safe_name(name: str) -> str:
    """Convert an arbitrary string into a valid Rust package / folder name."""
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = name.strip("_")
    # Rust package names must not start with a digit.
    if name and name[0].isdigit():
        name = "p_" + name
    return name


def create_rust_project(path: str, package_name: str):
    os.makedirs(os.path.join(path, "src"), exist_ok=True)

    cargo_toml = f"""[package]
name = "{package_name}"
version = "0.1.0"
edition = "2021"
"""
    with open(os.path.join(path, "Cargo.toml"), "w") as f:
        f.write(cargo_toml)

    if os.path.exists(TEMPLATE_FILE):
        shutil.copy(TEMPLATE_FILE, os.path.join(path, "src", "main.rs"))
    else:
        with open(os.path.join(path, "src", "main.rs"), "w") as f:
            f.write('fn main() { println!("Hello"); }\n')


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers["Content-Length"])
            data = self.rfile.read(length)
            problem = json.loads(data.decode())

            # Competitive Companion sends "group" as "Platform - Contest Name"
            # Strip the platform prefix (everything up to and including " - ")
            raw_group = problem.get("group", "")
            if " - " in raw_group:
                raw_group = raw_group.split(" - ", 1)[1]
            group = safe_name(raw_group)
            name = safe_name(problem.get("name", "problem"))

            parts = [p for p in [group, name] if p]
            folder = re.sub(r"_+", "_", "_".join(parts)).strip("_")

            path = os.path.join(PROBLEMS_DIR, folder)
            os.makedirs(path, exist_ok=True)

            create_rust_project(path, folder)

            # Save each sample as tests/N.in and tests/N.out
            tests = problem.get("tests", [])
            if tests:
                tests_dir = os.path.join(path, "tests")
                os.makedirs(tests_dir, exist_ok=True)
                for i, test in enumerate(tests, start=1):
                    with open(
                        os.path.join(tests_dir, f"{i}.in"), "w", encoding="utf-8"
                    ) as f:
                        f.write(test.get("input", ""))
                    with open(
                        os.path.join(tests_dir, f"{i}.out"), "w", encoding="utf-8"
                    ) as f:
                        f.write(test.get("output", ""))

            with open(os.path.join(path, "meta.json"), "w", encoding="utf-8") as f:
                json.dump(problem, f, indent=2)

            print(f"[✓] Created: {folder}  ({problem.get('name', '')})")
            print(f"[✓] Path:    {path}")
            print(f"[✓] Tests:   {len(tests)} sample(s)")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "path": path}).encode())

        except Exception as e:
            print(f"[✗] Error: {e}")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"status": "error", "message": str(e)}).encode()
            )

    def log_message(self, format, *args):
        pass  # Suppress default per-request HTTP log noise


if __name__ == "__main__":
    print(f"[i] BASE_DIR:     {BASE_DIR}")
    print(f"[i] PROBLEMS_DIR: {PROBLEMS_DIR}")
    server = HTTPServer(("127.0.0.1", 10043), Handler)
    print("[i] Listening on http://127.0.0.1:10043  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("\n[i] Server stopped.")
