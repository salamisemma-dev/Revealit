#!/usr/bin/env python3
"""bob runtime-check — golden-file / runtime contract checks for schema specs.

The validator proves a spec is well-formed and tied to a test. This goes one step
further for data work: it proves a schema spec's *contract actually behaves* by
running golden sample data through it. A schema spec can no longer "look valid" while
the real data shape drifts — golden samples that should pass must pass, and samples
that should fail must fail.

How it works:
- For each spec of type `schema`, extract the first ```json fenced block in its
  Contract section — that's the JSON Schema (a small, common subset).
- Look for golden samples under `<root>/golden/<spec-id>/valid/*.json` (must pass) and
  `<root>/golden/<spec-id>/invalid/*.json` (must fail).
- Validate each sample against the schema with a dependency-free checker.
- Error if a valid sample fails or an invalid sample passes. Warn if a schema spec has
  no golden samples (encouraged, not mandatory).

Usage:
    python bob_runtime_check.py [PROJECT_ROOT] [--json]
Exit 1 on any mismatch.

Supported JSON Schema subset (enough for data contracts, stdlib only): type, required,
properties, additionalProperties:false, enum, minLength, maxLength, minimum, maximum,
items. Document any spec needing more and extend here.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SPEC_JSON_RE = re.compile(r"```json\s*(.*?)```", re.DOTALL)

_TYPE_CHECKS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    # bool is a subclass of int in Python; exclude it from number/integer.
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "null": lambda v: v is None,
}


def json_schema_check(schema, instance, path="$"):
    """Return a list of human-readable validation errors (empty = valid)."""
    errors = []
    t = schema.get("type")
    if t:
        types = t if isinstance(t, list) else [t]
        if not any(_TYPE_CHECKS.get(tt, lambda v: True)(instance) for tt in types):
            errors.append(f"{path}: expected type {t}, got {type(instance).__name__}")
            return errors  # type wrong → deeper checks are noise

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in enum {schema['enum']}")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: longer than maxLength {schema['maxLength']}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: above maximum {schema['maximum']}")

    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}: missing required property '{req}'")
        props = schema.get("properties", {})
        for key, val in instance.items():
            if key in props:
                errors.extend(json_schema_check(props[key], val, f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: additional property '{key}' not allowed")

    if isinstance(instance, list) and "items" in schema:
        for i, item in enumerate(instance):
            errors.extend(json_schema_check(schema["items"], item, f"{path}[{i}]"))

    return errors


def extract_schema(spec_text):
    """Return the first JSON object in a ```json block, or None."""
    m = SPEC_JSON_RE.search(spec_text)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def _frontmatter_field(text, key):
    m = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def run(root: Path):
    errors, warnings = [], []
    specs_dir = root / "specs"
    if not specs_dir.is_dir():
        warnings.append("no specs/ directory — nothing to runtime-check.")
        return errors, warnings

    schema_specs = []
    for f in sorted(specs_dir.rglob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        if _frontmatter_field(text, "type") == "schema":
            sid = _frontmatter_field(text, "id")
            schema_specs.append((f.relative_to(root).as_posix(), sid, text))

    if not schema_specs:
        warnings.append("no schema specs found — runtime checks apply to schema specs.")
        return errors, warnings

    for rel, sid, text in schema_specs:
        # SQL/DDL or otherwise non-JSON contracts can opt out of golden checks with
        # frontmatter `runtime: manual` — their contract isn't a JSON Schema, so a
        # missing ```json block is intentional, not a gap.
        if (_frontmatter_field(text, "runtime") or "").lower() == "manual":
            warnings.append(
                f"{rel}: runtime: manual — golden checks intentionally skipped "
                "(non-JSON/SQL contract). Confirm a real test covers this schema."
            )
            continue
        schema = extract_schema(text)
        if schema is None:
            warnings.append(f"{rel}: no ```json schema block in Contract — can't runtime-check.")
            continue
        gdir = root / "golden" / (sid or "")
        valid_dir, invalid_dir = gdir / "valid", gdir / "invalid"
        samples = list(valid_dir.glob("*.json")) + list(invalid_dir.glob("*.json"))
        if not samples:
            warnings.append(
                f"{rel}: no golden samples under golden/{sid}/ (valid|invalid). "
                "Add some so the contract is checked against real data."
            )
            continue
        for vf in sorted(valid_dir.glob("*.json")):
            inst = json.loads(vf.read_text(encoding="utf-8"))
            errs = json_schema_check(schema, inst)
            if errs:
                errors.append(f"{rel}: golden VALID sample {vf.name} failed schema: {errs}")
        for invf in sorted(invalid_dir.glob("*.json")):
            inst = json.loads(invf.read_text(encoding="utf-8"))
            errs = json_schema_check(schema, inst)
            if not errs:
                errors.append(
                    f"{rel}: golden INVALID sample {invf.name} unexpectedly PASSED the "
                    "schema (the contract is too loose or the sample is wrong)."
                )
    return errors, warnings


def main(argv=None):
    ap = argparse.ArgumentParser(description="Golden-file runtime checks for schema specs.")
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    errors, warnings = run(root)

    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings}, indent=2))
    else:
        for w in warnings:
            print(f"WARN  {w}")
        for e in errors:
            print(f"ERROR {e}")
        print(f"\n{'FAIL' if errors else 'OK'}: runtime check — "
              f"{len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

