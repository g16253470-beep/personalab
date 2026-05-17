"""posthog_case — PostHog (open-source product analytics) as case study #1.

Translates publicly-available PostHog surfaces (product pages, docs,
pricing, changelog) into events a persona evaluates over a 5-day window.
"""

from examples.posthog_case.adapter import PostHogAdapter

__all__ = ["PostHogAdapter"]
