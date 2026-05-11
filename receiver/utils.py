import re


def safe_name(name: str) -> str:
    """Convert an arbitrary string into a valid Rust package / folder name."""
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = name.strip("_")
    # Rust package names must not start with a digit.
    if name and name[0].isdigit():
        name = "p_" + name
    return name
