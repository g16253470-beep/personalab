"""personalab CLI entry point.

Usage:
    personalab version
    personalab run --mode static|agentic|both \
        --personas DIR \
        --adapter signalstream \
        --db PATH \
        [--limit 30] [--days 7] [--concurrency 3] \
        [--out-dir ./reports]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path  # noqa: F401  (used below in _calibrate)

log = logging.getLogger("personalab")


def _build_product(name: str, args: argparse.Namespace):
    """Construct a ProductAdapter by name. Add new adapters here."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    if name == "signalstream":
        from examples.signalstream import SignalStreamAdapter
        if not args.db:
            raise SystemExit("signalstream adapter requires --db PATH")
        return SignalStreamAdapter(db_path=args.db)
    if name == "toy":
        from examples.toy import ToyAdapter
        return ToyAdapter()
    if name == "personalab-meta":
        from examples.personalab_meta import PersonaLabSelfAdapter
        return PersonaLabSelfAdapter()
    if name == "posthog":
        from examples.posthog_case import PostHogAdapter
        return PostHogAdapter()
    if name == "calcom":
        from examples.calcom_case import CalComAdapter
        return CalComAdapter()
    raise SystemExit(f"unknown adapter: {name}")


def _ns_swap_db(args: argparse.Namespace, new_db: str) -> argparse.Namespace:
    """Return a shallow copy of args with --db swapped (for AB mode)."""
    cp = argparse.Namespace(**vars(args))
    cp.db = new_db
    return cp


def _build_llms(spec: str):
    """Comma-separated spec → list[LLMAdapter]. e.g.
       'claude-cli'  → 1 adapter
       'claude-cli,openai:gpt-4o,gemini:gemini-2.5-pro' → 3 adapters
    """
    from personalab.adapters import build_llm
    out = []
    for s in spec.split(","):
        s = s.strip()
        if not s:
            continue
        try:
            out.append(build_llm(s))
        except (ImportError, RuntimeError, ValueError) as e:
            raise SystemExit(f"cannot build LLM '{s}': {e}")
    if not out:
        raise SystemExit("at least one LLM required")
    return out


async def _run(args: argparse.Namespace) -> int:
    from personalab.core.mode import TestMode  # noqa: F401  type hint use
    from personalab.core.persona import load_personas
    from personalab.modes import StaticMode, AgenticMode, JuryMode
    from personalab.reports import (StaticReporter, AgenticReporter,
                                       ComparisonReporter, ActionLoopReporter,
                                       JuryReporter)

    personas = load_personas(args.personas)
    if not personas:
        log.error("no personas found in %s", args.personas)
        return 2

    product = _build_product(args.adapter, args)
    llms = _build_llms(args.llm)
    llm = llms[0]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    static_result = None
    agentic_result = None
    jury_result = None

    # AB mode handled separately — needs second adapter
    if args.mode == "ab":
        from personalab.modes import ABMode
        from personalab.reports.ab import ABReporter
        if not args.db_b:
            raise SystemExit("ab mode requires --db-b PATH (second adapter source)")
        product_b = _build_product(args.adapter, _ns_swap_db(args, args.db_b))
        inner: TestMode
        if args.inner_mode == "static":
            inner = StaticMode(concurrency=args.concurrency,
                               retries=args.retries, timeout=args.timeout)
        else:
            inner = AgenticMode(days=args.days,
                                concurrency=max(1, args.concurrency // 2 or 1),
                                retries=args.retries, timeout=args.timeout)
        result = await ABMode(inner=inner, product_a=product,
                              product_b=product_b,
                              label_a=args.label_a,
                              label_b=args.label_b
                              ).run(personas, product, llm,
                                    config={"limit": args.limit})
        (out_dir / "ab_report.md").write_text(
            ABReporter().render(result), encoding="utf-8")
        (out_dir / "ab_result.json").write_text(
            json.dumps({"mode": result.mode, "metadata": result.metadata,
                        "results": result.results},
                       ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        log.info("ab report -> %s", out_dir / "ab_report.md")
        print(f"\n[OK] ab report written to: {out_dir.resolve()}")
        return 0

    # Stats mode handled separately — wraps another inner mode
    if args.mode == "stats":
        from personalab.modes import StatsMode
        from personalab.reports.stats import StatsReporter
        if args.inner_mode == "static":
            inner = StaticMode(concurrency=args.concurrency,
                               retries=args.retries, timeout=args.timeout)
        else:
            inner = AgenticMode(days=args.days,
                                concurrency=max(1, args.concurrency // 2 or 1),
                                retries=args.retries, timeout=args.timeout)
        result = await StatsMode(inner=inner, repeats=args.repeats
                                 ).run(personas, product, llm,
                                       config={"limit": args.limit})
        (out_dir / "stats_report.md").write_text(
            StatsReporter().render(result), encoding="utf-8")
        (out_dir / "stats_result.json").write_text(
            json.dumps({"mode": result.mode, "metadata": result.metadata,
                        "results": result.results},
                       ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        log.info("stats report -> %s", out_dir / "stats_report.md")
        print(f"\n[OK] stats report written to: {out_dir.resolve()}")
        return 0

    # Jury mode handled separately
    if args.mode == "jury":
        if len(llms) < 2:
            log.warning("jury mode with only 1 LLM is a sanity test; "
                        "pass --llm a,b,c for real cross-validation")
        jm = JuryMode(jury=llms, concurrency=args.concurrency,
                      retries=args.retries, timeout=args.timeout)
        jury_result = await jm.run(personas, product, llm,
                                    config={"limit": args.limit})
        JuryReporter(product_label=product.name).render_to_file(
            jury_result, out_dir / "jury_report.md"
        )
        (out_dir / "jury_result.json").write_text(
            json.dumps({"mode": jury_result.mode,
                        "metadata": jury_result.metadata,
                        "results": jury_result.results},
                       ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        log.info("jury report -> %s", out_dir / "jury_report.md")
        print(f"\n[OK] jury report written to: {out_dir.resolve()}")
        return 0

    if args.mode in ("static", "both"):
        log.info("running static mode (%d personas)", len(personas))
        sm = StaticMode(concurrency=args.concurrency,
                         retries=args.retries,
                         timeout=args.timeout)
        static_result = await sm.run(
            personas, product, llm,
            config={"limit": args.limit},
        )
        StaticReporter(product_label=product.name).render_to_file(
            static_result, out_dir / "static_report.md"
        )
        (out_dir / "static_result.json").write_text(
            json.dumps({"mode": static_result.mode,
                        "metadata": static_result.metadata,
                        "results": static_result.results},
                       ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        log.info("static report -> %s", out_dir / "static_report.md")

    if args.mode in ("agentic", "both"):
        log.info("running agentic mode (%d personas × %d days)",
                 len(personas), args.days)
        am = AgenticMode(days=args.days,
                          concurrency=max(1, args.concurrency // 2 or 1),
                          retries=args.retries,
                          timeout=args.timeout)
        agentic_result = await am.run(
            personas, product, llm,
            config={"event_limit": args.event_limit},
        )
        AgenticReporter(product_label=product.name).render_to_file(
            agentic_result, out_dir / "agentic_report.md"
        )
        (out_dir / "agentic_result.json").write_text(
            json.dumps({"mode": agentic_result.mode,
                        "metadata": agentic_result.metadata,
                        "results": agentic_result.results},
                       ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        log.info("agentic report -> %s", out_dir / "agentic_report.md")

    if args.mode == "both" and static_result and agentic_result:
        cmp_md = ComparisonReporter(product_label=product.name).render_dual(
            static_result, agentic_result
        )
        (out_dir / "comparison_report.md").write_text(cmp_md, encoding="utf-8")
        log.info("comparison report -> %s", out_dir / "comparison_report.md")

    # Action loop report — generated whenever we have at least one mode result
    if static_result or agentic_result:
        action_md = ActionLoopReporter(product_label=product.name)._render_combined(
            static=static_result, agentic=agentic_result
        )
        (out_dir / "action_loop.md").write_text(action_md, encoding="utf-8")
        log.info("action-loop report -> %s", out_dir / "action_loop.md")

    if args.html:
        from personalab.reports.html_renderer import render_dir_md_to_html
        rendered = render_dir_md_to_html(out_dir)
        log.info("html: rendered %d markdown files → .html", len(rendered))

    print(f"\n[OK] reports written to: {out_dir.resolve()}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="personalab",
                                  description="LLM persona testing framework")
    sub = ap.add_subparsers(dest="command", required=True)

    sub.add_parser("version")

    cal = sub.add_parser("calibrate",
                          help="L6: compare persona predictions to real users")
    cal.add_argument("--predictions", required=True,
                     help="path to a *_result.json produced by `run`")
    cal.add_argument("--truth", required=True,
                     help="path to real-users CSV or JSON (schema in "
                          "personalab.calibration.dataset)")
    cal.add_argument("--out", default="./reports/calibration_report.md")
    cal.add_argument("--maybe-as", default="yes", choices=["yes", "no"],
                     help="how to binarize 'maybe' predictions")

    run = sub.add_parser("run", help="run test modes against a product")
    run.add_argument("--mode", default="both",
                     choices=["static", "agentic", "both", "jury", "ab",
                              "stats"])
    run.add_argument("--personas", required=True,
                     help="directory containing *.md persona files")
    run.add_argument("--adapter", default="signalstream",
                     help="ProductAdapter name")
    run.add_argument("--db", default=None,
                     help="adapter-specific data source (sqlite path)")
    run.add_argument("--db-b", default=None,
                     help="(ab mode) second adapter data source")
    run.add_argument("--inner-mode", default="static",
                     choices=["static", "agentic"],
                     help="(ab/stats mode) inner mode to wrap")
    run.add_argument("--repeats", type=int, default=3,
                     help="(stats mode) number of repeated runs per persona")
    run.add_argument("--label-a", default="A",
                     help="(ab mode) human label for first product")
    run.add_argument("--label-b", default="B",
                     help="(ab mode) human label for second product")
    run.add_argument("--llm", default="claude-cli",
                     help="comma-separated LLM specs. Examples: "
                          "'claude-cli', 'openai:gpt-4o', "
                          "'claude-cli,openai:gpt-4o,gemini:gemini-2.5-pro'")
    run.add_argument("--limit", type=int, default=30,
                     help="static: number of recent events shown")
    run.add_argument("--event-limit", type=int, default=None,
                     help="agentic: cap on total events loaded")
    run.add_argument("--days", type=int, default=7,
                     help="agentic: simulated days")
    run.add_argument("--concurrency", type=int, default=3)
    run.add_argument("--retries", type=int, default=3)
    run.add_argument("--timeout", type=float, default=180.0)
    run.add_argument("--out-dir", default="./reports")
    run.add_argument("--html", action="store_true",
                     help="also render every *.md report to a sibling *.html")
    run.add_argument("--verbose", "-v", action="store_true")

    args = ap.parse_args(argv)

    if args.command == "version":
        from personalab import __version__
        print(f"personalab {__version__}")
        return 0

    if args.command == "calibrate":
        return _calibrate(args)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    return asyncio.run(_run(args))


def _calibrate(args: argparse.Namespace) -> int:
    from personalab.calibration import calibrate, load_real_users
    from personalab.reports.calibration import CalibrationReporter

    pred_path = Path(args.predictions)
    truth_path = Path(args.truth)
    data = json.loads(pred_path.read_text("utf-8"))
    predictions = data.get("results", data)  # accept raw list too
    real_users = load_real_users(truth_path)
    result = calibrate(predictions, real_users, maybe_as=args.maybe_as)
    md = CalibrationReporter().render(result)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    cm = result.subscribe
    print(f"[OK] calibration report: {out.resolve()}")
    print(f"     accuracy={cm.accuracy():.2%} f1={cm.f1():.2%} "
          f"price_mae={result.price_mae}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
