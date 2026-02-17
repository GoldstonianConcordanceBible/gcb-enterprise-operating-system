import json
import os
import sys

try:
    import jsonschema
except ImportError:
    print("Missing dependency: jsonschema\nInstall: pip install jsonschema")
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CANON_PATH = os.path.join(ROOT, "01-canon", "CANON_INDEX.json")
SCHEMA_PATH = os.path.join(ROOT, "01-canon", "SCHEMAS", "canon_index.schema.json")

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    canon = load_json(CANON_PATH)
    schema = load_json(SCHEMA_PATH)

    # Schema validation
    jsonschema.validate(instance=canon, schema=schema)

    # Integrity checks
    aliases = canon.get("resolver", {}).get("aliases", [])
    if not isinstance(aliases, list) or len(aliases) == 0:
        raise ValueError("resolver.aliases must be a non-empty list")

    seen = set()
    for a in aliases:
        key = a.get("alias", "").strip().lower()
        if not key:
            raise ValueError("Each alias entry must have 'alias'")
        if key in seen:
            raise ValueError(f"Duplicate alias found: {a.get('alias')}")
        seen.add(key)

        if not a.get("resolves_to"):
            raise ValueError(f"Alias '{a.get('alias')}' missing resolves_to")

    works = canon.get("works", [])
    if not isinstance(works, list):
        raise ValueError("works must be a list")

    print("✅ Canon validation passed.")
    print(f"Canon version: {canon.get('canon_version')}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Canon validation failed: {e}")
        sys.exit(1)