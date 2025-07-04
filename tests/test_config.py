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

@pytest.mark.parametrize(
    "provider, env_vars, should_raise",
    [
        (
            "S3",
            {
                "S3_ENDPOINT_URL": "e",
                "S3_ACCESS_KEY": "a",
                "S3_SECRET_KEY": "s",
                "S3_BUCKET_NAME": "b",
                "S3_REGION": "r",
            },
            False,
        ),
        (
            "S3",
            {
                "S3_ENDPOINT_URL": None,
                "S3_ACCESS_KEY": None,
                "S3_SECRET_KEY": None,
                "S3_BUCKET_NAME": None,
                "S3_REGION": None,
            },
            True,
        ),
    ],
)
def test_validate_env_vars_s3(monkeypatch, provider, env_vars, should_raise):
    cfg = reload_config(monkeypatch, API_KEY='x', **env_vars)
    if should_raise:
        with pytest.raises(ValueError):
            cfg.validate_env_vars(provider)
    else:
        cfg.validate_env_vars(provider)
