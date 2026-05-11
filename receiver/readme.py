import os


def create_readme(
    path: str,
    folder: str,
    problem: dict,
    tests: list,
    lang,
    platform: str = "",
    problem_code: str = "",
):
    title = problem.get("name", "Problem")
    url = problem.get("url", "")
    raw_group = problem.get("group", "")
    # Strip platform prefix to get just the contest name
    contest = raw_group.split(" - ", 1)[1].strip() if " - " in raw_group else raw_group
    time_limit = problem.get("timeLimit", "?")
    memory_limit = problem.get("memoryLimit", "?")

    lines = [
        f"# {title}",
        "",
    ]

    if platform:
        lines.append(f"**Platform:** {platform}  ")
    if problem_code:
        lines.append(f"**Problem Code:** {problem_code}  ")
    if platform or problem_code:
        lines.append("")

    lines += [
        f"**Contest:** {contest}  ",
        f"**Problem:** [{title}]({url})  " if url else f"**Problem:** {title}  ",
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
