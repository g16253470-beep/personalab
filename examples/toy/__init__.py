"""Toy ProductAdapter — minimal example to prove framework is product-agnostic.

This adapter holds events in memory; no databases, no domain knowledge.
Demonstrates the ProductAdapter contract in ~40 lines.
"""

from examples.toy.adapter import ToyAdapter

__all__ = ["ToyAdapter"]
