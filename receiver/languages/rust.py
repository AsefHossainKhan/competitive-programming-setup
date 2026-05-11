import os
import shutil

from config import TEMPLATE_RUST_FILE

SUBDIR = "rust"


def create_project(path: str, folder: str):
    os.makedirs(os.path.join(path, "src"), exist_ok=True)

    cargo_toml = f"""[package]
name = "{folder}"
version = "0.1.0"
edition = "2021"
"""
    with open(os.path.join(path, "Cargo.toml"), "w") as f:
        f.write(cargo_toml)

    if os.path.exists(TEMPLATE_RUST_FILE):
        shutil.copy(TEMPLATE_RUST_FILE, os.path.join(path, "src", "main.rs"))
    else:
        with open(os.path.join(path, "src", "main.rs"), "w") as f:
            f.write('fn main() { println!("Hello"); }\n')


def readme_commands(folder: str) -> list:
    return [
        "## Run",
        "",
        "### From repo root:",
        "```bash",
        f"cargo run -p {folder} < problems/rust/{folder}/tests/1.in",
        "```",
        "",
        "### Diff against expected output:",
        "```bash",
        f"cargo run -p {folder} < problems/rust/{folder}/tests/1.in | diff - problems/rust/{folder}/tests/1.out",
        "```",
    ]
