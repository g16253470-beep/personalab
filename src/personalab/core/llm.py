"""LLMAdapter: pluggable backend for one-shot prompt → text completion.

Concrete adapters (Anthropic API, OpenAI, Gemini) live in personalab.adapters.*
and are loaded as optional extras. The default ClaudeCLIAdapter shells out to
the `claude -p` CLI and requires no extra packages.
"""
from __future__ import annotations

import asyncio
import logging
import shutil
from abc import ABC, abstractmethod

log = logging.getLogger(__name__)


class LLMAdapter(ABC):
    """One-shot prompt → string. Async to allow concurrency across personas."""

    name: str = "base"

    @abstractmethod
    async def complete(self, prompt: str, timeout: float = 180.0) -> str:
        """Send prompt, return raw text reply. May raise on timeout / error."""


class ClaudeCLIAdapter(LLMAdapter):
    """Shells out to `claude -p` subprocess for each completion.

    Zero-dependency — works as long as Claude Code CLI is installed and on PATH.
    Each call spawns a fresh subprocess (no shared session state).
    """

    name = "claude-cli"

    def __init__(self, claude_binary: str | None = None,
                 extra_args: list[str] | None = None) -> None:
        self.binary = claude_binary or shutil.which("claude") or "claude"
        self.extra_args = list(extra_args or [])

    async def complete(self, prompt: str, timeout: float = 180.0) -> str:
        cmd = [self.binary, "-p", *self.extra_args]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(prompt.encode("utf-8")),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            raise TimeoutError(f"{self.name} timed out after {timeout}s")
        if proc.returncode != 0:
            err = stderr.decode("utf-8", errors="replace")
            raise RuntimeError(f"{self.name} exit {proc.returncode}: {err[:500]}")
        return stdout.decode("utf-8", errors="replace")
