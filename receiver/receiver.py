import os
import sys
import threading
import time
from http.server import HTTPServer

# Ensure sibling modules (config, handler, etc.) are importable regardless of CWD.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import BASE_DIR, PROBLEMS_DIR  # noqa: E402
from handler import Handler  # noqa: E402

if __name__ == "__main__":
    print(f"[i] BASE_DIR:     {BASE_DIR}")
    print(f"[i] PROBLEMS_DIR: {PROBLEMS_DIR}")
    server = HTTPServer(("127.0.0.1", 10043), Handler)
    print("[i] Listening on http://127.0.0.1:10043  (Ctrl+C to stop)")

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

