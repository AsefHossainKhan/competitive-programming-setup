import argparse
import os
import sys
import threading
import time
from http.server import HTTPServer

# Ensure sibling modules (config, handler, etc.) are importable regardless of CWD.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import BASE_DIR, PORT, PROBLEMS_DIR  # noqa: E402
from handler import Handler  # noqa: E402
from languages import CHOICES, REGISTRY  # noqa: E402


def make_handler(lang_module):
    """Return a Handler subclass with `language` pre-bound to lang_module."""
    return type("BoundHandler", (Handler,), {"language": lang_module})


def pick_language_interactive() -> str:
    print("\nSelect a language:")
    for i, name in enumerate(CHOICES, start=1):
        print(f"  {i}. {name}")
    while True:
        choice = input("Enter number or name: ").strip().lower()
        if choice in REGISTRY:
            return choice
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(CHOICES):
                return CHOICES[idx]
        print(f"  Invalid choice. Enter one of: {', '.join(CHOICES)}")


def main():
    parser = argparse.ArgumentParser(
        description="Competitive Companion receiver",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "lang",
        nargs="?",
        choices=CHOICES,
        metavar="LANG",
        help=f"Language to use ({', '.join(CHOICES)}). Omit to choose interactively.",
    )
    args = parser.parse_args()

    lang_name = args.lang if args.lang else pick_language_interactive()
    lang_module = REGISTRY[lang_name]

    print(f"\n[i] Language:    {lang_name}")
    print(f"[i] BASE_DIR:     {BASE_DIR}")
    print(f"[i] PROBLEMS_DIR: {PROBLEMS_DIR}")

    server = HTTPServer(("127.0.0.1", PORT), make_handler(lang_module))
    print(f"[i] Listening on http://127.0.0.1:{PORT}  (Ctrl+C to stop)")

    # Run server in a daemon thread so the main thread stays free to catch
    # Ctrl+C — Git Bash on Windows can't interrupt Python's select() directly.
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
        print("\n[i] Server stopped.")


if __name__ == "__main__":
    main()
