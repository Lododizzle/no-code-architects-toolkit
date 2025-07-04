import json
import importlib
from pathlib import Path
import time
import pytest

import generate_docs


def test_load_config(tmp_path):
    cfg_path = Path(generate_docs.__file__).parent / ".env_shell.json"
    data = {"ANTHROPIC_API_KEY": "k", "API_DOC_OUTPUT_DIR": str(tmp_path)}

    with open(cfg_path, "w") as f:
        json.dump(data, f)

    try:
        importlib.reload(generate_docs)
        api_key, out_dir = generate_docs.load_config()
        assert api_key == "k"
        assert out_dir == str(tmp_path)
    finally:
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



@pytest.mark.parametrize(
    "contents, expect_error",
    [
        ("{", True),
        ("{\"ANTHROPIC_API_KEY\": \"k\"}", False),
    ],
)
def test_load_config_edge(tmp_path, contents, expect_error):
    cfg_path = Path(generate_docs.__file__).parent / ".env_shell.json"
    cfg_path.write_text(contents)

    try:
        if expect_error:
            with pytest.raises(SystemExit):
                importlib.reload(generate_docs)
                generate_docs.load_config()
        else:
            importlib.reload(generate_docs)
            generate_docs.load_config()
    finally:
        cfg_path.unlink()
