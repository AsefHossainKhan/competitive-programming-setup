import re


def platform_prefix(platform: str) -> str:
    """Return a short identifier for a platform, used as a folder name prefix.

    Examples: 'Codeforces' → 'cf', 'LeetCode' → 'lc', anything else → 'prefix'.
    """
    pl = platform.lower()
    if "codeforces" in pl:
        return "cf"
    if "leetcode" in pl:
        return "lc"
    return "prefix"


def safe_name(name: str, digit_prefix: str = "p") -> str:
    """Convert an arbitrary string into a valid Rust package / folder name.

    digit_prefix is prepended (with an underscore) when the result would
    otherwise start with a digit, which is invalid for Rust package names.
    """
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = name.strip("_")
    # Rust package names must not start with a digit.
    if name and name[0].isdigit():
        name = digit_prefix + "_" + name
    return name


def extract_platform(group: str) -> str:
    """Return the platform name from a Competitive Companion group string.

    Competitive Companion formats group as "Platform - Contest Name".
    Returns the full group string if no separator is found.
    """
    if " - " in group:
        return group.split(" - ", 1)[0].strip()
    return group.strip()


def extract_problem_code(platform: str, name: str, url: str) -> str:
    """Return a short problem code such as '4A', '227C', or '42'.

    Returns an empty string when no code can be determined.

    Supported platforms
    -------------------
    Codeforces
        URL patterns:
          https://codeforces.com/problemset/problem/4/A   → "4A"
          https://codeforces.com/contest/227/problem/C    → "227C"
    LeetCode
        Problem name often starts with the number:
          "42. Trapping Rain Water"                       → "42"
    """
    platform_lower = platform.lower()

    if "codeforces" in platform_lower:
        # /problemset/problem/<id>/<letter>
        m = re.search(r"/problem/(\d+)/([A-Za-z]\d*)", url)
        if m:
            return m.group(1) + m.group(2).upper()
        # /contest/<id>/problem/<letter>
        m = re.search(r"/contest/(\d+)/problem/([A-Za-z]\d*)", url)
        if m:
            return m.group(1) + m.group(2).upper()

    if "leetcode" in platform_lower:
        # Name may start with "42. Title" or "42 Title"
        m = re.match(r"^(\d+)[.\s]", name)
        if m:
            return m.group(1)

    return ""
