import json

from src.config.setting import Setting


class DummySetting(Setting):
    # avoid auto-loading config in __init__ if base class does that
    def __init__(self):
        self._config = {}


def test_load_config_from_explicit_path(tmp_path):
    cfg = {"api_keys": {"daum": {"api_key": "abc123"}}}
    p = tmp_path / "config.json"
    p.write_text(json.dumps(cfg), encoding="utf-8")

    s = DummySetting()
    # call load_config with explicit path to avoid relying on default CWD
    s.load_config(str(p))

    assert s.get("api_keys.daum.api_key", None) == "abc123"


def test_get_missing_key_returns_default(tmp_path):
    cfg = {"some": {"value": 1}}
    p = tmp_path / "config.json"
    p.write_text(json.dumps(cfg), encoding="utf-8")

    s = DummySetting()
    s.load_config(str(p))

    assert s.get("does.not.exist", "fallback") == "fallback"
