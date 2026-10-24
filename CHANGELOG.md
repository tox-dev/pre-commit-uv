# Changelog

<!-- towncrier release notes start -->

<a name="release-4-4-0"></a>

## 4.4.0 (2026-10-10)

<a name="release-4-4-0-added"></a>

### Added

- Require Python 3.11 or newer ([#183](https://github.com/tox-dev/pre-commit-uv/pull/183)) by
  [@gaborbernat](https://github.com/gaborbernat).
- Use Python 3.15 by default ([#183](https://github.com/tox-dev/pre-commit-uv/pull/183)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-3-0"></a>

## 4.3.0 (2026-07-20)

<a name="release-4-3-0-added"></a>

### Added

- Support Python 3.15 ([#164](https://github.com/tox-dev/pre-commit-uv/pull/164)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-2-2"></a>

## 4.2.2 (2026-06-19)

<a name="release-4-2-2-fixed"></a>

### Fixed

- Handle truncated `version_info` values in uv's `pyvenv.cfg`
  ([#153](https://github.com/tox-dev/pre-commit-uv/pull/153)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-2-1"></a>

## 4.2.1 (2026-02-18)

<a name="release-4-2-1-fixed"></a>

### Fixed

- Seed pip into hook environments ([#114](https://github.com/tox-dev/pre-commit-uv/pull/114)) by
  [@gaborbernat](https://github.com/gaborbernat).
- Detect calls through `python -m pre_commit` ([#115](https://github.com/tox-dev/pre-commit-uv/pull/115)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-2-0"></a>

## 4.2.0 (2025-10-09)

<a name="release-4-2-0-added"></a>

### Added

- Support Python 3.14 ([#86](https://github.com/tox-dev/pre-commit-uv/pull/86)) by
  [@ssbarnea](https://github.com/ssbarnea).
- End Python 3.9 support ([#91](https://github.com/tox-dev/pre-commit-uv/pull/91)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-1-5"></a>

## 4.1.5 (2025-08-27)

<a name="release-4-1-5-changes"></a>

### Changes

- Use the current project's uv configuration ([#79](https://github.com/tox-dev/pre-commit-uv/pull/79)) by
  [@aaravind100](https://github.com/aaravind100).

<a name="release-4-1-4"></a>

## 4.1.4 (2024-10-29)

<a name="release-4-1-4-fixed"></a>

### Fixed

- Respect `UV_PYTHON` and fall back to `sys.executable` ([#29](https://github.com/tox-dev/pre-commit-uv/pull/29)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-1-3"></a>

## 4.1.3 (2024-09-23)

<a name="release-4-1-3-fixed"></a>

### Fixed

- Patch pre-commit when invoked by `git commit` ([#18](https://github.com/tox-dev/pre-commit-uv/pull/18)) by
  [@florianfischer91](https://github.com/florianfischer91).

<a name="release-4-1-2"></a>

## 4.1.2 (2024-09-18)

<a name="release-4-1-1"></a>

## 4.1.1 (2024-09-08)

<a name="release-4-1-1-added"></a>

### Added

- Support Python 3.13 ([#12](https://github.com/tox-dev/pre-commit-uv/pull/12)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-1-0"></a>

## 4.1.0 (2024-08-12)

<a name="release-4-1-0-changes"></a>

### Changes

- Show pre-commit-uv and uv versions in `--version` output ([#7](https://github.com/tox-dev/pre-commit-uv/pull/7)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-0-3"></a>

## 4.0.3 (2024-08-08)

<a name="release-4-0-3-fixed"></a>

### Fixed

- Pass the caller's Python to uv ([#5](https://github.com/tox-dev/pre-commit-uv/pull/5)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-0-2"></a>

## 4.0.2 (2024-08-07)

<a name="release-4-0-2-documentation"></a>

### Documentation

- Add installation instructions ([commit](https://github.com/tox-dev/pre-commit-uv/commit/fdb8619)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-0-1"></a>

## 4.0.1 (2024-08-07)

<a name="release-4-0-1-performance"></a>

### Performance

- Avoid patching import overhead ([#2](https://github.com/tox-dev/pre-commit-uv/pull/2)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-0-1-documentation"></a>

### Documentation

- Extend the README ([#2](https://github.com/tox-dev/pre-commit-uv/pull/2)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-4-0-0"></a>

## 4.0.0 (2024-08-05)

<a name="release-4-0-0-added"></a>

### Added

- Publish the first pre-commit-uv release ([#1](https://github.com/tox-dev/pre-commit-uv/pull/1)) by
  [@gaborbernat](https://github.com/gaborbernat).
