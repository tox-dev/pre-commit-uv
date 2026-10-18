# Changelog

<!-- towncrier release notes start -->

## 4.4.0 (2026-10-10)

<!-- Release notes generated using configuration in .github/release.yaml at main -->

### What's Changed

- 🔧 chore: batch dependency updates weekly on Tuesday by @gaborbernat in
  https://github.com/tox-dev/pre-commit-uv/pull/172
- 👷 ci: pin ubuntu-26.04 and bump dependencies by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/181
- feat(python): require 3.11 and default to 3.15 by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/183

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.3.0...4.4.0

## 4.3.0 (2026-07-20)

No user-facing changes. This tag includes Python 3.15 CI coverage and dependency updates.

## 4.2.2 (2026-06-19)

<!-- Release notes generated using configuration in .github/release.yaml at main -->

### What's Changed

- 🔧 chore(tox): migrate tox.ini to tox.toml by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/116
- Migrate type checking from mypy to ty by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/117
- Move from extras to dependency-groups by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/118
- Align dependency versions across projects by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/120
- Add permissions to workflows by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/121
- Move SECURITY.md to .github/SECURITY.md by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/122
- Add missing .github config files by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/123
- Standardize .github files to .yaml suffix by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/126
- 🔒 ci(workflows): add zizmor security auditing by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/131
- Drop redundant int cast in \_new_main by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/148
- Tolerate uv truncated pyvenv.cfg version_info by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/153

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.2.1...4.2.2

## 4.2.1 (2026-02-18)

<!-- Release notes generated using configuration in .github/release.yml at main -->

### What's Changed

- 🐛 fix(venv): seed pip into hook environments by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/114
- 🐛 fix(patch): detect python -m pre_commit by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/115

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.2.0...4.2.1

## 4.2.0 (2025-10-09)

<!-- Release notes generated using configuration in .github/release.yml at main -->

### What's Changed

- fix: add support for python 3.14 by @ssbarnea in https://github.com/tox-dev/pre-commit-uv/pull/86
- Drop 3.9 support by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/91

### New Contributors

- @ssbarnea made their first contribution in https://github.com/tox-dev/pre-commit-uv/pull/86

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.1.5...4.2.0

## 4.1.5 (2025-08-27)

<!-- Release notes generated using configuration in .github/release.yml at main -->

### What's Changed

- Use current project config for uv by @aaravind100 in https://github.com/tox-dev/pre-commit-uv/pull/79

### New Contributors

- @aaravind100 made their first contribution in https://github.com/tox-dev/pre-commit-uv/pull/79

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.1.4...4.1.5

## 4.1.4 (2024-10-29)

<!-- Release notes generated using configuration in .github/release.yml at main -->

### What's Changed

- Respect UV_PYTHON and fallback to sys.executable by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/29

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.1.3...4.1.4

## 4.1.3 (2024-09-23)

<!-- Release notes generated using configuration in .github/release.yml at main -->

### What's Changed

- Patch pre-commit also when called due to a git commit by @florianfischer91 in
  https://github.com/tox-dev/pre-commit-uv/pull/18

### New Contributors

- @florianfischer91 made their first contribution in https://github.com/tox-dev/pre-commit-uv/pull/18

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.1.2...4.1.3

## 4.1.2 (2024-09-18)

<!-- Release notes generated using configuration in .github/release.yml at main -->

### What's Changed

- Improve the CI by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/16

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.1.1...4.1.2

## 4.1.1 (2024-09-08)

<!-- Release notes generated using configuration in .github/release.yml at main -->

### What's Changed

- Declare 3.13 support by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/12

### New Contributors

- @dependabot made their first contribution in https://github.com/tox-dev/pre-commit-uv/pull/10

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.1.0...4.1.1

## 4.1.0 (2024-08-12)

<!-- Release notes generated using configuration in .github/release.yml at main -->

### What's Changed

- Specify pre-commit-uv and uv version in --version by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/7

### New Contributors

- @pre-commit-ci made their first contribution in https://github.com/tox-dev/pre-commit-uv/pull/6

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.0.3...4.1.0

## 4.0.3 (2024-08-08)

<!-- Release notes generated using configuration in .github/release.yml at main -->

### What's Changed

- Ensure uv knows caller Python by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/5

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.0.2...4.0.3

## 4.0.2 (2024-08-07)

<!-- Release notes generated using configuration in .github/release.yml at main -->

Add installation instructions.

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.0.1...4.0.2

## 4.0.1 (2024-08-07)

<!-- Release notes generated using configuration in .github/release.yml at main -->

### What's Changed

- Avoid patching import overheads and extend README by @gaborbernat in https://github.com/tox-dev/pre-commit-uv/pull/2

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/compare/4.0.0...4.0.1

## 4.0.0 (2024-08-05)

<!-- Release notes generated using configuration in .github/release.yml at main -->

- First version (using `4.0.0` as version to not break previous fork release of `3.8`).

**Full Changelog**: https://github.com/tox-dev/pre-commit-uv/commits/4.0.0
