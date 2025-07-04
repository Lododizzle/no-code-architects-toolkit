import importlib
import sys
import pytest


def reload_config(monkeypatch, **env):
    for key, value in env.items():
        if value is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, value)
    if 'config' in sys.modules:
        del sys.modules['config']
    return importlib.import_module('config')


def test_validate_env_vars_success(monkeypatch, tmp_path):
    cfg = reload_config(
        monkeypatch,
        API_KEY='x',
        GCP_BUCKET_NAME='b',
        GCP_SA_CREDENTIALS='c',
    )
    cfg.validate_env_vars('GCP')


def test_validate_env_vars_missing(monkeypatch):
    cfg = reload_config(
        monkeypatch,
        API_KEY='x',
        GCP_BUCKET_NAME=None,
        GCP_SA_CREDENTIALS=None,
    )
    with pytest.raises(ValueError):
        cfg.validate_env_vars('GCP')
