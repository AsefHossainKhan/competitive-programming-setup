# Competitive Programming

A local automation setup for competitive programming that integrates with the [Competitive Companion](https://github.com/jmerle/competitive-companion) browser extension. When you click the Companion button on a problem page, it automatically creates a ready-to-code project with the correct folder structure, a template solution file, and all sample test cases.

---

## Requirements

| Dependency | Purpose |
|---|---|
| **Python 3.8+** | Runs the receiver server |
| **Rust + Cargo** | Required only if solving problems in Rust |
| **Competitive Companion** | Browser extension that sends problem data to the server |

---

## How It Works

```
Browser (Competitive Companion)
        │
        │  HTTP POST  (problem JSON)
        ▼
receiver/main.py  ←  listening on port 10043
        │
        ├─ Parses problem name, group, platform, URL, and sample tests
        ├─ Creates problems/<lang>/<folder>/
        │       ├─ src/main.rs  (or src/main.py)
        │       ├─ Cargo.toml  (Rust only)
        │       ├─ tests/1.in, 1.out, 2.in, 2.out, …
        │       ├─ meta.json   (raw JSON from Companion)
        │       └─ README.md   (problem info + run commands)
        └─ Prints confirmation to the terminal
```

1. You start the receiver (`python receiver/main.py`).
2. You open a problem on Codeforces, LeetCode, or any other supported site.
3. You click the **Competitive Companion** button in your browser.
4. The extension POSTs the problem data to `http://127.0.0.1:10043`.
5. The receiver scaffolds a complete project in `problems/<lang>/<folder>/`.

---

## Supported Languages

| Language | Folder | Template |
|---|---|---|
| **Rust** | `problems/rust/<folder>/` | `templates/main.rs` |
| **Python** | `problems/python/<folder>/` | `templates/main.py` |

Rust problems are automatically registered as members of the root Cargo workspace (`Cargo.toml`), so you can build and run any of them with `cargo run -p <folder>` from the repo root.

---

## Port Configuration

The receiver listens on **port `10043`** by default. This is set in `receiver/config.py`:

```python
PORT = 10043
```

Competitive Companion must be configured to send to the **same port**. To change it:

1. Open `receiver/config.py` and update `PORT` to your desired value.
2. Open the Competitive Companion extension settings in your browser and set the **"Custom port"** field to the same value.

---

## Folder Naming

By default the folder name is derived from the full contest and problem name, e.g.:

```
codeforces_beta_round_4_div_2_only_a_watermelon
```

You can switch to a shorter code-based name (e.g. `cf_4a`, `lc_42`) by setting the flag in `receiver/config.py`:

```python
# Default — verbose name built from contest + problem title
USE_PROBLEM_CODE_AS_FOLDER = False

# Short code-based name (e.g. cf_4a, lc_42)
# Falls back to the verbose name when no code can be extracted
USE_PROBLEM_CODE_AS_FOLDER = True
```

**Platform prefixes used in code mode:**

| Platform | Prefix |
|---|---|
| Codeforces | `cf` |
| LeetCode | `lc` |
| Other | `prefix` |

---

## Quick Start — End-to-End Example

Here is a complete walkthrough using [Codeforces 4A — Watermelon](https://codeforces.com/problemset/problem/4/A) as an example.

**1. Install Competitive Companion**
Install the browser extension ([Chrome](https://chrome.google.com/webstore/detail/competitive-companion/cjnmckjndlpiamhfimnnjmnckgghkjbl) / [Firefox](https://addons.mozilla.org/en-US/firefox/addon/competitive-companion/)) and set the custom port to `10043` (should already be the default) in its options.

**2. Start the receiver**
```bash
python receiver/main.py rust
```
```
[i] Language:    rust
[i] Listening on http://127.0.0.1:10043  (Ctrl+C to stop)
```

**3. Open the problem and click the extension**
Navigate to `https://codeforces.com/problemset/problem/4/A` in your browser and click the Competitive Companion button. The terminal confirms the project was created:
```
[✓] Created: codeforces_beta_round_4_div_2_only_a_watermelon
[✓] Path:    .../problems/rust/codeforces_beta_round_4_div_2_only_a_watermelon
[✓] Tests:   1 sample(s)
```

**4. Write your solution**
Open `problems/rust/codeforces_beta_round_4_div_2_only_a_watermelon/src/main.rs` and implement the solution.

**5. Test it against the sample**
```bash
cargo run -p codeforces_beta_round_4_div_2_only_a_watermelon \
  < problems/rust/codeforces_beta_round_4_div_2_only_a_watermelon/tests/1.in \
  | diff - problems/rust/codeforces_beta_round_4_div_2_only_a_watermelon/tests/1.out
```
No output means your answer matches the expected output. Done — submit.

> **Tip:** Enable `USE_PROBLEM_CODE_AS_FOLDER = True` in `config.py` to get the shorter folder name `cf_4a` instead.

---

## Running the Receiver

```bash
# Interactive language selection
python receiver/main.py

# Or pass the language directly
python receiver/main.py rust
python receiver/main.py python
```

The server starts and waits for Competitive Companion to send problems. Press **Ctrl+C** to stop it.

---

## Running a Solution

### Rust

```bash
# Run with sample input
cargo run -p <folder> < problems/rust/<folder>/tests/1.in

# Diff against expected output
cargo run -p <folder> < problems/rust/<folder>/tests/1.in | diff - problems/rust/<folder>/tests/1.out
```

### Python

```bash
# Run with sample input
python problems/python/<folder>/src/main.py < problems/python/<folder>/tests/1.in

# Diff against expected output
python problems/python/<folder>/src/main.py < problems/python/<folder>/tests/1.in | diff - problems/python/<folder>/tests/1.out
```

---

## Competitive Companion Setup

1. Install the **Competitive Companion** extension for [Chrome](https://chrome.google.com/webstore/detail/competitive-companion/cjnmckjndlpiamhfimnnjmnckgghkjbl) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/competitive-companion/).
2. Open the extension options.
3. Set the **"Custom port"** to `10043` (or whatever `PORT` is set to in `receiver/config.py`).
4. Make sure the receiver is running **before** you click the Companion button on a problem page.

---

## Project Structure

```
competitive-programming/
├── Cargo.toml              # Workspace — includes all problems/rust/*/
├── templates/
│   ├── main.rs             # Rust solution template
│   └── main.py             # Python solution template
├── problems/
│   ├── rust/               # Auto-generated Rust problem folders
│   └── python/             # Auto-generated Python problem folders
└── receiver/
    ├── main.py             # Entry point — starts the HTTP server
    ├── config.py           # PORT, folder settings, paths
    ├── handler.py          # HTTP request handler
    ├── utils.py            # Name sanitization and code extraction
    ├── readme.py           # Per-problem README generator
    └── languages/
        ├── rust.py         # Rust project scaffolding
        └── python.py       # Python project scaffolding
```
