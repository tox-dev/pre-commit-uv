# Contributing

## Check a change

Use tox for the Python test matrix and package checks:

```bash
tox run -e 3.15,type,pkg_meta
tox run -e fix
```

The `pkg_meta` environment builds an sdist and wheel, then runs Twine and check-wheel-contents on them. The pull request
workflow also tests Python 3.11 through 3.15 and free-threaded 3.15.

## Add release news

For a change that affects users, add a Markdown fragment such as `changelog.d/+seed-pip.bugfix.md`:

```markdown
Seed pip into hook environments that need it.
```

Use one fragment per distinct change; a pull request may include several fragments in different categories. Choose
`feature` for new behavior or Python support additions and removals, `change` for changed behavior, `bugfix` for fixes,
and `doc` for user documentation. Use `security`, `performance`, `deprecation`, `removal`, `breaking`, or `packaging`
only when the change affects users in that way. The release job adds the squash-merged pull request number and credits
its human authors. You do not need a pull request number when you create the fragment.

For maintenance with no user-facing change, apply the `skip news` label. You can add it after opening the pull request;
the news check reruns when labels change. Maintenance bot pull requests without fragments receive the label
automatically. A bot pull request that supplies a fragment must pass the same fragment validation as a human one.

## Make a release

Run **Prepare release** on `main`. The default `auto` option selects a major version for a `breaking` fragment, a minor
version for a `feature` fragment, and a patch version for other categories. The workflow builds and formats
`CHANGELOG.md`, runs `prek` on the result, and uses the repository-scoped App to push the release commit and tag. The
tag workflow builds the distribution, publishes it to PyPI through trusted publishing, then creates the GitHub Release
from the tagged changelog. The workflow does not ask for a version string.
