# tests/test_reproducibility.py
"""Regression tests for dskit.reproducibility.

These cover the lower-level `run_experiment` function that exposes a
config-driven experiment runner used by `Toolkit.run`. Earlier versions
had a `NameError: best_model` bug because the trained estimator was
assigned to a local variable named `model` while the rest of the
function referenced `best_model`. These tests would have failed loudly.
"""

import json
import pandas as pd
import pytest

from dskit.reproducibility import run_experiment, run_experiment_logged


@pytest.fixture
def tiny_csv(tmp_path, sample_df):
    """Write the sample_df to a CSV that `run_experiment` can load."""
    path = tmp_path / "advertising.csv"
    sample_df.to_csv(path, index=False)
    return path


@pytest.fixture
def base_config(tiny_csv, tmp_path):
    """Minimal valid config for `run_experiment_logged`."""
    return {
        "experiment_id": "test_run",
        "seed": 42,
        "data": {
            "path": str(tiny_csv),
            "target": "Sales",
            "read_kwargs": {"index_col": None},  # CSV has no index column
        },
        "splitting": {"test_size": 0.3},
        "preprocessing": {
            "scaling": {
                "columns": ["TV", "Radio", "Newspaper"],
                "method": "standard",
            },
        },
        "model": {"class": "LinearRegression", "params": {}},
        "output": {
            "experiments_dir": str(tmp_path / "experiments"),
        },
    }


def test_run_experiment_logged_completes_without_nameerror(base_config):
    """Regression: previously crashed with `NameError: best_model`."""
    result = run_experiment_logged(base_config)
    assert result["status"] == "success"
    assert "train_r2" in result["metrics"]
    assert "test_r2" in result["metrics"]


def test_run_experiment_logged_writes_artifacts(base_config):
    """Regression: `joblib.dump(best_model, ...)` previously crashed."""
    from pathlib import Path
    run_experiment_logged(base_config)
    exp_dir = Path(base_config["output"]["experiments_dir"]) / base_config["experiment_id"]
    assert (exp_dir / "model.joblib").exists()
    assert (exp_dir / "pipeline.joblib").exists()
    metrics = json.loads((exp_dir / "metrics.json").read_text())
    assert "train_r2" in metrics


def test_run_experiment_logged_respects_index_col_none(tmp_path, sample_df):
    """Regression: config with no index column should keep all columns."""
    path = tmp_path / "advertising_no_index.csv"
    sample_df.to_csv(path, index=False)
    cfg = {
        "experiment_id": "no_idx",
        "seed": 7,
        "data": {
            "path": str(path),
            "target": "Sales",
            "read_kwargs": {"index_col": None},
        },
        "splitting": {"test_size": 0.3},
        "preprocessing": {
            "scaling": {
                "columns": ["TV", "Radio", "Newspaper"],
                "method": "standard",
            }
        },
        "model": {"class": "Ridge", "params": {"alpha": 1.0}},
        "output": {"experiments_dir": str(tmp_path / "experiments")},
    }
    result = run_experiment_logged(cfg)
    assert result["status"] == "success"


def test_run_experiment_returns_best_model_metadata(tiny_csv, tmp_path):
    """`run_experiment` should return structured output with metrics.

    Unlike `run_experiment_logged`, this function expects `config['models']`
    as a dict of `{name: class_string}` and selects the best by MSE.
    """
    cfg = {
        "experiment_id": "best_of_two",
        "seed": 42,
        "data": {
            "path": str(tiny_csv),
            "target": "Sales",
            "read_kwargs": {"index_col": None},
        },
        "splitting": {"test_size": 0.3},
        "preprocessing": {
            "scaling": {"columns": ["TV", "Radio", "Newspaper"]},
        },
        "models": {
            "linear": {"class": "LinearRegression", "params": {}},
            "ridge":  {"class": "Ridge", "params": {"alpha": 1.0}},
        },
        "output": {"experiments_dir": str(tmp_path / "experiments")},
    }
    result = run_experiment(cfg)
    assert result["status"] == "success"
    assert result["best_model_name"] in {"linear", "ridge"}
    assert "metrics" in result
    assert "artifact_dir" in result