"""SignalStream (okx_pulse) reference ProductAdapter.

Read events from a local sqlite db produced by the okx_pulse SignalStream bot.
Serves as a real-world example of how to implement personalab.core.ProductAdapter.
"""

from examples.signalstream.adapter import SignalStreamAdapter

__all__ = ["SignalStreamAdapter"]
