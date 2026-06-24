# Changelog

All notable changes to dskit are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com).

## [1.0.0] - 2026-06-24

### Added
- Initial stable release
- All core modules: data_io, eda, preprocessing, splitting,
  pipeline, feature_engineering, modeling, persistence,
  artifacts, reproducibility, config, performance
- CLI entry point: `dskit-run`

### Fixed
- `reproducibility.run_experiment()` no longer raises `NameError`
  for `best_model` (was previously named `model`).
- `pipeline.run_full_pipeline()` now honours `data.read_kwargs`
  from config (previously ignored, defaulting to `index_col=0`).
- `pipeline.run_full_pipeline()` no longer requires
  `output.logs_dir`, `production_dir`, `registry_path`, or
  `experiments_dir` (all now have sensible defaults).
- `artifacts.save_experiment` / `archive_experiment` /
  `update_status` and several `pipeline.run_full_pipeline`
  prints no longer crash on Windows consoles by emitting
  Unicode (`→`, `²`, `—`, `×`) via `print()`.
- `pyproject.toml` now declares `descripstats>=0.1.1` as a
  required dependency (was previously missing, causing
  `ModuleNotFoundError` on `import dskit` for fresh installs).

## [0.5.0] - 2025-04-20

### Added
- Polars backend support in `data_io.py`
- `performance.py` module with profiling and optimization utilities

## [0.4.0] - 2025-03-10

### Added
- Configuration system and environment profiles (Chapter 17)

## [0.3.0] - 2025-02-25

### Added
- Reproducibility layer and artifact management (Chapters 14–15)

## [0.2.0] - 2025-01-30

### Added
- Artifact management and versioning (Chapter 14)

## [0.1.0] - 2024-12-01

### Added
- Initial release — core preprocessing and data access modules (Chapters 4–12)
