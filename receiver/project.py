import os
import shutil

from config import TEMPLATE_FILE


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
