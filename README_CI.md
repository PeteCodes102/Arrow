Continuous Integration (CI) for this repository — quick tutorial

What I added

- A GitHub Actions workflow: `.github/workflows/python-tests.yml`.
  - It runs automatically on `push` and `pull_request` events targeting the
    `main` or `master` branch.
  - The workflow sets up Python (3.11, 3.12, 3.13) and runs `pytest`.

Why CI matters (plain English)

CI stands for Continuous Integration. It means:
- Every time you push code (or open/update a pull request), GitHub runs an automated
  job that checks your code.
- In this repo the check is "run the tests with pytest".
- If tests fail, GitHub shows a red cross and the detailed logs so you can fix
  the issue before merging code into the main branch.

This helps catch bugs early, ensures code quality, and makes collaboration safer.

How the workflow works (step-by-step)

1. You push or open a PR to `main`/`master`.
2. GitHub Actions triggers the workflow.
3. The job checks out your code, sets up Python, installs dependencies, and runs `pytest`.
4. The workflow completes and reports pass/fail on the pull request and on the GitHub
   Actions tab for the repository.

Where to see results

- On GitHub, open the repository and click the "Actions" tab. There you'll see
  workflow runs, their status, and logs for each step.
- Inside a pull request, GitHub shows the workflow status near the merge box —
  you can expand it to see the logs.

Badge (optional)

You can add a status badge to your README to show the latest test status. Once you
have the repository owner and name, add this Markdown to your README:

```markdown
[![Python tests](https://github.com/<OWNER>/<REPO>/actions/workflows/python-tests.yml/badge.svg)](https://github.com/<OWNER>/<REPO>/actions/workflows/python-tests.yml)
```

Replace `<OWNER>` and `<REPO>` with your GitHub username/organization and repo name.

How to make tests run locally (quick commands)

- Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows (cmd.exe)
.venv\\Scripts\\activate
# macOS / Linux
source .venv/bin/activate
```

- Install dependencies (the workflow tries to install from `requirements.txt` if
  present; otherwise it installs the minimal test deps):

```bash
python -m pip install --upgrade pip
python -m pip install pytest pandas numpy
```

- Run the tests:

```bash
python -m pytest -q
```

Troubleshooting tips (common failures)

- Missing dependencies: If the workflow fails while importing a package, add
  it to `requirements.txt` at the project root so the workflow installs it.
- Failing tests: Open the Actions log for the failing run, expand the "Run tests"
  step and inspect the pytest output. The traceback shows which assertion failed.
- Environment differences: If tests pass locally but fail on CI, ensure your
  `requirements.txt` pins compatible versions or add a `requirements-dev.txt`.

Security note

- Don't put secrets (API keys, private tokens) directly in the workflow YAML. Use
  GitHub repository secrets and reference them from the workflow when necessary.

Next steps I can help with

- Add a requirements-dev.txt and pin versions for stable CI runs.
- Add a status badge to the README with your repo details.
- Add code coverage reporting (e.g., using Coverage + Codecov or GitHub Actions).

If you'd like one of those, tell me which and I'll add it.
