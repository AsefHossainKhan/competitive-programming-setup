import os


def create_readme(path: str, folder: str, problem: dict, tests: list, lang):
    title = problem.get("name", "Problem")
    url = problem.get("url", "")
    raw_group = problem.get("group", "")
    time_limit = problem.get("timeLimit", "?")
    memory_limit = problem.get("memoryLimit", "?")

    lines = [
        f"# {title}",
        "",
        f"**Contest:** {raw_group}  ",
        f"**Problem:** [{title}]({url})  " if url else "",
        f"**Limits:** {time_limit} ms / {memory_limit} MB  ",
        "",
        "---",
        "",
        *lang.readme_commands(folder),
        "",
        "---",
        "",
        "## Sample Tests",
        "",
    ]

    for i, test in enumerate(tests, start=1):
        lines += [
            f"### Sample {i}",
            "",
            "**Input:**",
            "```",
            test.get("input", "").strip(),
            "```",
            "",
            "**Expected Output:**",
            "```",
            test.get("output", "").strip(),
            "```",
            "",
        ]

    with open(os.path.join(path, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
