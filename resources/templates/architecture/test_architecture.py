"""
GENERIC ARCHITECTURAL INVARIANT & AI GUARDRAIL TESTS (Python / Pytest)

Core Principle:
"An AI agent can drift from prose in a markdown file, but it cannot ignore
a failing unit test in the terminal (FAIL) or a blocked git commit."

Customize the configuration sets below to enforce your project's specific invariants.
"""

import os
import re
from pathlib import Path

# ==============================================================================
# 1. PROJECT INVARIANT CONFIGURATION (Customize for your stack & rules)
# ==============================================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
EXCLUDED_DIRS = {".git", ".venv", "venv", "__pycache__", ".agents", "dist", "build"}

# Banned dependencies (insecure, obsolete, or bloated packages)
BANNED_PACKAGES = {"pickle5"}

# ==============================================================================
# 2. SOURCE FILE CRAWLER
# ==============================================================================

def get_source_files(extension=".py"):
    files = []
    for root, dirs, filenames in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for f in filenames:
            if f.endswith(extension) and not f.startswith("test_"):
                files.append(Path(root) / f)
    return files


# ==============================================================================
# 3. ARCHITECTURAL INVARIANT TEST SUITE
# ==============================================================================

def test_zero_leak_no_hardcoded_secrets():
    """Pillar 1 (Zero-Leak): Verify no API keys, private tokens, or credentials are committed."""
    secret_patterns = [
        re.compile(r"sk-[a-zA-Z0-9]{20,}"),
        re.compile(r"ghp_[a-zA-Z0-9]{30,}"),
        re.compile(r"AIzaSy[a-zA-Z0-9_-]{33}"),
        re.compile(r"BEGIN (RSA|EC|PRIVATE) KEY"),
        re.compile(r"""(password|secret|api_key|apiKey)\s*[:=]\s*["'][a-zA-Z0-9_!@#$%^&*()+=]{8,}["']""", re.IGNORECASE),
    ]

    for py_file in get_source_files(".py"):
        content = py_file.read_text(encoding="utf-8", errors="ignore")
        for pattern in secret_patterns:
            match = pattern.search(content)
            assert match is None, (
                f"Security violation in {py_file.relative_to(ROOT_DIR)}: Potential hardcoded secret found."
            )


def test_anti_ai_cliches_no_superfluous_emojis():
    """Pillar 2 (Visual Tone): Ensure clean CLI/UI strings without emoji clutter."""
    emoji_pattern = re.compile(r"[\U0001F300-\U0001F6FF\U0001F900-\U0001F9FF\U00002600-\U000026FF]")

    for py_file in get_source_files(".py"):
        lines = py_file.read_text(encoding="utf-8", errors="ignore").splitlines()
        for idx, line in enumerate(lines, 1):
            if line.strip().startswith("#"):
                continue
            assert not emoji_pattern.search(line), (
                f"Style violation: Decorative emoji detected in {py_file.relative_to(ROOT_DIR)}:{idx}. Maintain a sober, professional interface."
            )


def test_dependency_diet_guardrail():
    """Pillar 3 (Dependency Diet): Audit pyproject.toml / requirements.txt against unvetted packages."""
    req_file = ROOT_DIR / "requirements.txt"
    pyproject = ROOT_DIR / "pyproject.toml"

    checked_content = ""
    if req_file.exists():
        checked_content += req_file.read_text(encoding="utf-8")
    if pyproject.exists():
        checked_content += pyproject.read_text(encoding="utf-8")

    for pkg in BANNED_PACKAGES:
        assert pkg not in checked_content.lower(), (
            f"Dependency violation: Prohibited package '{pkg}' found in dependency definitions."
        )
