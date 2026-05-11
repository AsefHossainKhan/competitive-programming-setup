import json
import os
import re
from http.server import BaseHTTPRequestHandler

from config import PROBLEMS_DIR
from utils import safe_name
from project import create_rust_project
from readme import create_readme


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
                    with open(os.path.join(tests_dir, f"{i}.in"), "w", encoding="utf-8") as f:
                        f.write(test.get("input", ""))
                    with open(os.path.join(tests_dir, f"{i}.out"), "w", encoding="utf-8") as f:
                        f.write(test.get("output", ""))

            with open(os.path.join(path, "meta.json"), "w", encoding="utf-8") as f:
                json.dump(problem, f, indent=2)

            create_readme(path, folder, problem, tests)

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
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())

    def log_message(self, format, *args):
        pass  # Suppress default per-request HTTP log noise
