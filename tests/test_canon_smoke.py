import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON_PATH = os.path.join(ROOT, "01-canon", "CANON_INDEX.json")

def test_canon_file_exists():
    assert os.path.exists(CANON_PATH)

def test_canon_has_version():
    with open(CANON_PATH, "r", encoding="utf-8") as f:
        canon = json.load(f)
    assert "canon_version" in canon
    assert isinstance(canon["canon_version"], str)