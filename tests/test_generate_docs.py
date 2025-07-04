import json
import importlib
from pathlib import Path
import time


import generate_docs


def test_load_config(tmp_path, monkeypatch):
    cfg_path = Path(generate_docs.__file__).parent / '.env_shell.json'
    data = {"ANTHROPIC_API_KEY": "k", "API_DOC_OUTPUT_DIR": str(tmp_path)}
    with open(cfg_path, 'w') as f:
        json.dump(data, f)
    importlib.reload(generate_docs)
    api_key, out_dir = generate_docs.load_config()
    assert api_key == 'k'
    assert out_dir == str(tmp_path)
    cfg_path.unlink()


def test_should_skip_doc_generation(tmp_path):
    test_file = tmp_path / 'f.md'
    test_file.write_text('x')
    assert generate_docs.should_skip_doc_generation(test_file) is True
    old = time.time() - 90000
    test_file.touch()
    import os
    os.utime(test_file, (old, old))
    assert generate_docs.should_skip_doc_generation(test_file) is False
    assert generate_docs.should_skip_doc_generation(test_file, force=True) is False
