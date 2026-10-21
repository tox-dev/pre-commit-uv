# pre-commit-uv

[![PyPI](https://img.shields.io/pypi/v/pre-commit-uv?style=flat-square)](https://pypi.org/project/pre-commit-uv)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/pre-commit-uv?style=flat-square)](https://pypi.org/project/pre-commit-uv)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pre-commit-uv?style=flat-square)](https://pypi.org/project/pre-commit-uv)
[![Downloads](https://static.pepy.tech/badge/pre-commit-uv/month)](https://pepy.tech/project/pre-commit-uv)
[![PyPI - License](https://img.shields.io/pypi/l/pre-commit-uv?style=flat-square)](https://opensource.org/licenses/MIT)
[![check](https://github.com/tox-dev/pre-commit-uv/actions/workflows/check.yaml/badge.svg)](https://github.com/tox-dev/pre-commit-uv/actions/workflows/check.yaml)

Use `uv` to create virtual environments and install packages for `pre-commit`.

[Changelog](CHANGELOG.md)

[Contributing](CONTRIBUTING.md)

## Installation

With pipx:

```shell
pipx install pre-commit
pipx inject pre-commit pre-commit-uv
```

With uv:

```shell
uv tool install pre-commit --with pre-commit-uv --force-reinstall
```

## Why?

`pre-commit-uv` uses uv to create and seed hook environments. Caching the pre-commit directory avoids this work on later
runs, but the first install still needs it. This benchmark used this project's hooks with a warm uv cache:

```shell
❯ hyperfine  'pre-commit install-hooks' 'pre-commit-uv install-hooks'
Benchmark 1: pre-commit install-hooks
  Time (mean ± σ):     54.132 s ±  8.827 s    [User: 15.424 s, System: 9.359 s]
  Range (min … max):   45.972 s … 66.506 s    10 runs

Benchmark 2: pre-commit-uv install-hooks
  Time (mean ± σ):     41.695 s ±  7.395 s    [User: 7.614 s, System: 6.133 s]
  Range (min … max):   32.198 s … 58.467 s    10 runs

Summary
  pre-commit-uv install-hooks ran 1.30 ± 0.31 times faster than pre-commit install-hooks
```

## Configuration

Once installed, `pre-commit-uv` uses uv by default. Set `DISABLE_PRE_COMMIT_UV_PATCH` to use pre-commit's normal
installation path instead.

The patch loads when the process appears to be running pre-commit. If detection misses a call, set
`FORCE_PRE_COMMIT_UV_PATCH` and report the value of `sys.argv` in an issue. `DISABLE_PRE_COMMIT_UV_PATCH` takes
precedence when both variables are set.
