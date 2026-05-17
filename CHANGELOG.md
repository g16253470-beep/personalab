# CHANGELOG

## 0.2.0 — 2026-05-18

**Breaking**: default `personas/` directory now contains 12 generic SaaS dev-tool personas (founder / growth PM / researcher / VC / indie hacker / consultant / OSS maintainer / AI safety / corporate PM / no-code / data lead / designer). The original 12 SignalStream crypto-trader personas moved to `personas_signalstream/` for users running the bundled signalstream example. **If you were running `--personas ./personas` against the signalstream adapter, switch to `--personas ./personas_signalstream`.**

### Added

- **PostHog case study adapter** (`examples/posthog_case/`) — 7-day evaluation journey using publicly-available PostHog product surfaces. Now the recommended SaaS adapter template.
- **HTML report renderer** — pass `--html` to `personalab run` and every `.md` report gets a sibling self-contained `.html` (works offline, no JS, ready to email).
- **`personalab calibrate` CLI** — compare persona predictions to real user CSV/JSON (L6 calibration, was SDK-only in 0.1.0).
- **`--mode ab` / `--mode stats`** wired into CLI (were SDK-only in 0.1.0). New flags: `--db-b`, `--inner-mode`, `--repeats`, `--label-a`, `--label-b`.
- **Anthropic-API guard** — `build_llm("anthropic-api:...")` now raises by default to encourage using `claude-cli` subscription. Set `PERSONALAB_ALLOW_CLAUDE_API=1` to override.
- **4 new personas** in `personas/`: `09_corporate_pm`, `10_no_code_user`, `11_data_team_lead`, `12_designer_lead`.
- **Toy adapter** (`examples/toy/`) — 40-line minimal reference for contract docs.
- **personalab-meta adapter** (`examples/personalab_meta/`) — point personalab at itself, ship with self-test reports.
- **`docs/QUICKSTART.md`** — 5-minute install + first run path.

### Changed

- README rewritten — removed SignalStream framing, added "Honest disclaimers" section. The product description is now domain-agnostic.
- `docs/ARCHITECTURE.md` / `ADAPTER_GUIDE.md` / `PERSONA_WRITING.md` — SignalStream demoted from main example to "event-stream template", PostHog becomes the SaaS-template reference.
- `pyproject.toml` — added `html` optional dependency (`personalab[html]` for `markdown>=3.5`).
- `cli.py` — `_build_product` now recognizes `toy`, `posthog`, `personalab-meta` adapters in addition to `signalstream`.

### Fixed

- Pyflakes cleaned: unused imports removed, f-strings without placeholders fixed, duplicate `tempfile` import in test main block removed.
- `core/parsing.py` no longer imports unused `Any` type.

### Removed

- `examples/signalstream/__init__.py` docstring mention of "SOLE place SignalStream knowledge lives" tightened — that's still true but framed cleaner.

## 0.1.0 — 2026-05-17

Initial release. L1–L7 framework: 5 test modes (Static, Agentic, Jury, AB, Stats), 4 LLM backends (Claude CLI, Anthropic API, OpenAI, Gemini), 8 report renderers, calibration vs real-user data, full SignalStream reference adapter. 12 SignalStream crypto-trader personas as default. ~3800 lines of Python, 6 end-to-end smoke tests.
