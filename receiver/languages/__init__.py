from . import rust, python  # noqa: F401 – imported for side-effect-free registry population

REGISTRY = {
    "rust": rust,
    "python": python,
}

CHOICES = list(REGISTRY)
