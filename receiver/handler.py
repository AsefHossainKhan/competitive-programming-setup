import json
import os
import re
from http.server import BaseHTTPRequestHandler

from config import PROBLEMS_DIR, USE_PROBLEM_CODE_AS_FOLDER
from utils import safe_name, extract_platform, extract_problem_code, platform_prefix
from readme import create_readme


class Handler(BaseHTTPRequestHandler):
    language = None  # set by make_handler() in main.py

    def do_POST(self):
        try:
            length = int(self.headers["Content-Length"])
            data = self.rfile.read(length)
            problem = json.loads(data.decode())

            # Competitive Companion sends "group" as "Platform - Contest Name"
            raw_group = problem.get("group", "")
            platform = extract_platform(raw_group)
            problem_name = problem.get("name", "problem")
            url = problem.get("url", "")
            problem_code = extract_problem_code(platform, problem_name, url)

            # Strip the platform prefix to get only the contest name
            contest_part = raw_group.split(" - ", 1)[1] if " - " in raw_group else raw_group
            group = safe_name(contest_part)
            name = safe_name(problem_name)

            if USE_PROBLEM_CODE_AS_FOLDER and problem_code:
                folder = safe_name(problem_code, digit_prefix=platform_prefix(platform))
            else:
                parts = [p for p in [group, name] if p]
                folder = re.sub(r"_+", "_", "_".join(parts)).strip("_")

            path = os.path.join(PROBLEMS_DIR, self.language.SUBDIR, folder)
            os.makedirs(path, exist_ok=True)

            self.language.create_project(path, folder)

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

            create_readme(path, folder, problem, tests, self.language, platform, problem_code)

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
