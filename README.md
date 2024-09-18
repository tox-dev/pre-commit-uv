# pre-commit-uv

[![PyPI](https://img.shields.io/pypi/v/pre-commit-uv?style=flat-square)](https://pypi.org/project/pre-commit-uv)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/pre-commit-uv?style=flat-square)](https://pypi.org/project/pre-commit-uv)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pre-commit-uv?style=flat-square)](https://pypi.org/project/pre-commit-uv)
[![Downloads](https://static.pepy.tech/badge/pre-commit-uv/month)](https://pepy.tech/project/pre-commit-uv)
[![PyPI - License](https://img.shields.io/pypi/l/pre-commit-uv?style=flat-square)](https://opensource.org/licenses/MIT)
[![check](https://github.com/tox-dev/pre-commit-uv/actions/workflows/check.yaml/badge.svg)](https://github.com/tox-dev/pre-commit-uv/actions/workflows/check.yaml)

Use `uv` to create virtual environments and install packages for `pre-commit`.

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

Compared to upstream `pre-commit` will speed up the initial seed operation. In general, upstream recommends caching the
`pre-commit` cache, however, that is not always possible and is still helpful to have a more performant initial cache
creation., Here's an example of what you could expect demonstrated on this project's own pre-commit setup (with a hot
`uv` cache):

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

Once installed will use `uv` out of box, however the `DISABLE_PRE_COMMIT_UV_PATCH` environment variable if is set it
will work as an escape hatch to disable the new behavior.

To avoid interpreter startup overhead of the patching, we only perform this when we detect you calling `pre-commit`.
Should this logic fail you can force the patching by setting the `FORCE_PRE_COMMIT_UV_PATCH` variable. Should you
experience this please raise an issue with the content of the `sys.argv`. Note that `DISABLE_PRE_COMMIT_UV_PATCH` will
overwrite this flag should both be set.
