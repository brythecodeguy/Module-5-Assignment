import pytest
from decimal import Decimal
from pathlib import Path

from app.calculator_config import CalculatorConfig, get_project_root
from app.exceptions import ConfigurationError


def test_get_project_root_points_to_repo_root():
    root = get_project_root()
    assert (root / "app").exists()


def test_default_fallbacks_use_expected_defaults(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    monkeypatch.delenv("CALCULATOR_MAX_HISTORY_SIZE", raising=False)
    monkeypatch.delenv("CALCULATOR_AUTO_SAVE", raising=False)
    monkeypatch.delenv("CALCULATOR_PRECISION", raising=False)
    monkeypatch.delenv("CALCULATOR_MAX_INPUT_VALUE", raising=False)
    monkeypatch.delenv("CALCULATOR_DEFAULT_ENCODING", raising=False)

    cfg = CalculatorConfig()
    assert cfg.max_history_size == 1000
    assert cfg.auto_save is True
    assert cfg.precision == 10
    assert str(cfg.max_input_value) == str(Decimal("1e999"))
    assert cfg.default_encoding == "utf-8"


def test_environment_overrides(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "500")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "8")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "1000")
    monkeypatch.setenv("CALCULATOR_DEFAULT_ENCODING", "utf-16")
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "test_logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "test_history"))
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(tmp_path / "test_history" / "test_history.csv"))
    monkeypatch.setenv("CALCULATOR_LOG_FILE", str(tmp_path / "test_logs" / "test_log.log"))

    cfg = CalculatorConfig()

    assert cfg.max_history_size == 500
    assert cfg.auto_save is False
    assert cfg.precision == 8
    assert cfg.max_input_value == Decimal("1000")
    assert cfg.default_encoding == "utf-16"
    assert cfg.log_dir == (tmp_path / "test_logs").resolve()
    assert cfg.history_dir == (tmp_path / "test_history").resolve()
    assert cfg.history_file == (tmp_path / "test_history" / "test_history.csv").resolve()
    assert cfg.log_file == (tmp_path / "test_logs" / "test_log.log").resolve()


def test_custom_configuration_overrides_env(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "500")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "8")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "1000")
    monkeypatch.setenv("CALCULATOR_DEFAULT_ENCODING", "utf-16")

    cfg = CalculatorConfig(
        max_history_size=300,
        auto_save=True,
        precision=5,
        max_input_value=Decimal("500"),
        default_encoding="ascii",
    )
    assert cfg.max_history_size == 300
    assert cfg.auto_save is True
    assert cfg.precision == 5
    assert cfg.max_input_value == Decimal("500")
    assert cfg.default_encoding == "ascii"


def test_directory_defaults_from_base_dir(tmp_path, monkeypatch):
    monkeypatch.delenv("CALCULATOR_LOG_DIR", raising=False)
    monkeypatch.delenv("CALCULATOR_HISTORY_DIR", raising=False)
    cfg = CalculatorConfig(base_dir=tmp_path)

    assert cfg.log_dir == (tmp_path / "logs").resolve()
    assert cfg.history_dir == (tmp_path / "history").resolve()


def test_file_defaults_from_base_dir(tmp_path, monkeypatch):
    monkeypatch.delenv("CALCULATOR_HISTORY_FILE", raising=False)
    monkeypatch.delenv("CALCULATOR_LOG_FILE", raising=False)
    cfg = CalculatorConfig(base_dir=tmp_path)

    assert cfg.history_file == (tmp_path / "history" / "calculator_history.csv").resolve()
    assert cfg.log_file == (tmp_path / "logs" / "calculator.log").resolve()


def test_validate_invalid_max_history_size_raises(tmp_path):
    with pytest.raises(ConfigurationError, match="max_history_size must be positive"):
        CalculatorConfig(base_dir=tmp_path, max_history_size=-1)


def test_validate_invalid_precision_raises(tmp_path):
    with pytest.raises(ConfigurationError, match="precision must be positive"):
        CalculatorConfig(base_dir=tmp_path, precision=-1)


def test_validate_invalid_max_input_value_raises(tmp_path):
    with pytest.raises(ConfigurationError, match="max_input_value must be positive"):
        CalculatorConfig(base_dir=tmp_path, max_input_value=Decimal("-1"))


def test_validate_invalid_encoding_raises(tmp_path):
    with pytest.raises(ConfigurationError, match="default_encoding must not be empty"):
        CalculatorConfig(base_dir=tmp_path, default_encoding="  ")


@pytest.mark.parametrize("raw, expected", [("true", True), ("1", True), ("false", False), ("0", False)])
def test_auto_save_env_parsing(tmp_path, monkeypatch, raw, expected):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", raw)
    cfg = CalculatorConfig(auto_save=None)
    assert cfg.auto_save is expected