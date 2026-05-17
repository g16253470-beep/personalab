# Release v0.2.0 — PyPI publish steps

Build artifacts are ready in `dist/`:

```
dist/personalab-0.2.0-py3-none-any.whl   (~55 KB)
dist/personalab-0.2.0.tar.gz             (~46 KB)
```

`twine check` passed both files.

## To actually publish (requires PyPI account + token)

### 1. (one-time) Create PyPI account + API token

- Sign up at https://pypi.org (and https://test.pypi.org for the dry-run target)
- In Account settings → API tokens, create one scoped to the `personalab` project (or initially to "Entire account" until the project exists)
- Save the token (starts with `pypi-`)

### 2. (recommended) Dry-run to Test PyPI first

```bash
python -m twine upload --repository testpypi dist/* \
  --username __token__ \
  --password pypi-AgENdGVz...   # your testpypi token
```

Then validate the install:

```bash
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            personalab==0.2.0
personalab version
```

### 3. Publish to real PyPI

```bash
python -m twine upload dist/* \
  --username __token__ \
  --password pypi-AgENd...   # your real PyPI token
```

After publish anyone in the world can `pip install personalab` and get this build.

### 4. (post-publish) Tag the release in git

```bash
git tag -a v0.2.0 -m "v0.2.0: PostHog case study + HTML renderer + SaaS personas + no-vaporware README"
git push origin v0.2.0
```

(Skip if this repo isn't a git repo yet — see "First-time git init" below.)

## First-time git init (if needed)

`G:/gpt/personalab` isn't a git repo yet. Before pushing to GitHub:

```bash
cd G:/gpt/personalab
git init
git add .
git commit -m "v0.2.0 initial public release"
git branch -M main
# create empty repo on github.com first, then:
git remote add origin https://github.com/<your-username>/personalab.git
git push -u origin main
git tag -a v0.2.0 -m "v0.2.0"
git push origin v0.2.0
```

## Tokens NOT to commit

`.gitignore` already excludes `.env`, but **never** commit:

- PyPI tokens (`pypi-...`)
- Anthropic/Gemini/OpenAI keys
- `dist/*` (regeneratable; many people exclude it)

## Post-release checklist

- [ ] PyPI page renders correctly (description, classifiers, project URLs)
- [ ] `pip install personalab` succeeds in a clean venv
- [ ] `personalab run --help` shows all 6 modes
- [ ] At least one HN/Twitter/Indie Hackers announcement
- [ ] GitHub Discussions enabled
- [ ] First issue/discussion seeded by you so the repo doesn't look dead
