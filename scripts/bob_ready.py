#!/usr/bin/env python3
"""bob ready — is this project BOB-ready? The adoption gate / fail-fast anti-vibe check.

Anti-vibe-coding only works if "build X" is *blocked* until the project has the
discipline in place. This script is that gate: it checks the concrete readiness
criteria and exits non-zero if any are missing, so CI (or the BOB workflow itself)
refuses to proceed on an un-specced project.

Criteria:
  1. constitution.md present (the supreme contract)
  2. at least one APPROVED spec
  3. strict validator passes (structure + traceability + assertion evidence)
  4. runtime/golden checks pass (no errors)
  5. a test suite is present (tests/, src/__tests__, or common test/spec files)
  6. test command passes (default; use --no-run-tests only for diagnosis)
  7. AGENTS.md present (DOX context)

Usage:
    python bob_ready.py [PROJECT_ROOT] [--json] [--no-run-tests]
Exit 0 only if every criterion passes.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bob_validate as bv  # noqa: E402
import bob_runtime_check as rc  # noqa: E402

SKIP_DIRS = {
    ".git",
    ".github",
    ".claude",
    ".vercel",
    "_archive",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    "coverage",
}
TEST_FILE_RE = re.compile(r"(^test_.*\.py$|.*(_test|\.test|\.spec)\.(py|js|mjs|cjs|ts|tsx|jsx)$)")


def _count_approved_specs(root: Path) -> int:
    specs = root / "specs"
    if not specs.is_dir():
        return 0
    n = 0
    for f in specs.rglob("*.md"):
        if f.name == "AGENTS.md":
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if re.search(r"^status:\s*approved\s*$", text, re.MULTILINE):
            n += 1
    return n


def _is_skipped(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    return any(part in SKIP_DIRS for part in rel.parts)


def _has_test_suite(root: Path):
    if (root / "tests").is_dir():
        return True, "tests/"
    if (root / "src" / "__tests__").is_dir():
        return True, "src/__tests__/"
    for candidate in root.rglob("*"):
        if _is_skipped(candidate, root):
            continue
        try:
            if candidate.is_file() and TEST_FILE_RE.match(candidate.name):
                return True, str(candidate.relative_to(root)).replace("\\", "/")
        except OSError:
            continue
    return False, "no tests/, src/__tests__, or *.(test|spec) files found"


def _detect_test_command(root: Path):
    """Return (cmd, label, shell) or (None, reason, False)."""
    package_json = root / "package.json"
    if package_json.is_file():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8", errors="replace"))
            if isinstance(data.get("scripts"), dict) and data["scripts"].get("test"):
                return "npm test --silent", "npm test", True
        except json.JSONDecodeError:
            if '"test"' in package_json.read_text(encoding="utf-8", errors="replace"):
                return "npm test --silent", "npm test", True
    if (root / "tests").is_dir():
        return [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], "python -m unittest discover -s tests -v", False
    if list(root.glob("test_*.py")):
        return [sys.executable, "-m", "unittest", "discover", "-v"], "python -m unittest discover -v", False
    return None, "no supported test command detected", False


def _run_tests(root: Path):
    cmd, label, shell = _detect_test_command(root)
    if cmd is None:
        return False, label
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
            shell=shell,
        )
    except FileNotFoundError as exc:
        return False, f"{label}: not found ({exc})"
    except OSError as exc:
        return False, f"{label}: could not run ({exc})"
    except subprocess.TimeoutExpired:
        return False, f"{label} timed out after 120s"
    if proc.returncode == 0:
        return True, f"{label}: passed"
    tail = "\n".join((proc.stdout or "").splitlines()[-8:])
    return False, f"{label}: FAILED with exit {proc.returncode}: {tail}"


def assess(root: Path, run_tests: bool = True):
    """Return a list of (criterion, passed, detail)."""
    results = []

    results.append(("constitution.md present", (root / "constitution.md").is_file(), ""))

    approved = _count_approved_specs(root)
    results.append(("at least one approved spec", approved >= 1, f"{approved} found"))

    v_errors, _ = bv.validate(root, strict=True)
    results.append(("strict validator passes (structure + traceability)", not v_errors,
                    f"{len(v_errors)} error(s)"))

    r_errors, _ = rc.run(root)
    results.append(("runtime/golden checks pass", not r_errors, f"{len(r_errors)} error(s)"))

    has_tests, test_detail = _has_test_suite(root)
    results.append(("test suite present", has_tests, test_detail))

    if run_tests:
        tests_ok, tests_detail = _run_tests(root)
        results.append(("test command passes", tests_ok, tests_detail))
    else:
        results.append(("test command passes", True, "skipped by --no-run-tests"))

    results.append(("AGENTS.md present (DOX)", (root / "AGENTS.md").is_file(), ""))

    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description="BOB adoption / readiness gate.")
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--run-tests", action="store_true",
                    help="deprecated no-op: tests run by default")
    ap.add_argument("--no-run-tests", action="store_true",
                    help="diagnostic escape hatch; CI should not use this")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    results = assess(root, run_tests=not args.no_run_tests)
    ready = all(p for _, p, _ in results)

    if args.json:
        print(json.dumps({
            "root": str(root), "ready": ready, "run_tests": not args.no_run_tests,
            "criteria": [{"name": n, "passed": p, "detail": d} for n, p, d in results],
        }, indent=2))
    else:
        print(f"BOB readiness: {root}\n")
        for name, passed, detail in results:
            mark = "[x]" if passed else "[ ]"
            tail = f"  ({detail})" if detail else ""
            print(f"  {mark} {name}{tail}")
        print(f"\n{'READY' if ready else 'NOT READY'} — "
              f"{sum(p for _, p, _ in results)}/{len(results)} criteria met.")
        if not ready:
            print("Fail-fast: do not generate code until every box is checked. "
                  "See docs/ADOPTION.md.")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())

