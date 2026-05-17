"""LLM adapters: ClaudeCLI (built-in), AnthropicAPI, OpenAI, Gemini (optional).

Concrete adapters are imported lazily from their submodules to avoid forcing
users to install all optional SDKs.
"""

__all__ = ["build_llm"]


def build_llm(spec: str):
    """Construct an LLMAdapter from a string spec.

    Spec forms:
        claude-cli                       — ClaudeCLI (no deps, uses Claude subscription)
        anthropic-api[:model]            — DISABLED by default (set PERSONALAB_ALLOW_CLAUDE_API=1 to override)
        openai[:model]                   — OpenAI, default gpt-4o
        gemini[:model]                   — Gemini, default gemini-2.5-pro
    """
    import os
    backend, _, model = spec.partition(":")
    backend = backend.strip().lower()
    if backend == "claude-cli":
        from personalab.core.llm import ClaudeCLIAdapter
        return ClaudeCLIAdapter()
    if backend == "anthropic-api":
        if not os.environ.get("PERSONALAB_ALLOW_CLAUDE_API"):
            raise RuntimeError(
                "anthropic-api is disabled by personal policy "
                "(only use the Claude subscription via 'claude-cli'). "
                "To override (NOT recommended): "
                "export PERSONALAB_ALLOW_CLAUDE_API=1"
            )
        from personalab.adapters.anthropic_api import AnthropicAPIAdapter
        kwargs = {"model": model} if model else {}
        return AnthropicAPIAdapter(**kwargs)
    if backend == "openai":
        from personalab.adapters.openai_api import OpenAIAdapter
        kwargs = {"model": model} if model else {}
        return OpenAIAdapter(**kwargs)
    if backend == "gemini":
        from personalab.adapters.gemini_api import GeminiAdapter
        kwargs = {"model": model} if model else {}
        return GeminiAdapter(**kwargs)
    raise ValueError(f"unknown llm spec: {spec}")
