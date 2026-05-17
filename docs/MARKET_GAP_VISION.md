# Vision: personalab as Market Gap Finder

**Status**: draft. Designs `MarketGapMode` — the largest planned expansion of personalab to date. Target: v0.4.0 (M3-M4 in roadmap).

## The pitch

> Today, personalab evaluates **one product** through N personas.
> Tomorrow, personalab evaluates **a whole market** through N personas and tells you which gap is the highest-confidence one to fill.

This reframes personalab from "product feedback tool" (1-2 uses per product) to "thesis engine" (every founder / VC / corp innovation lab uses it monthly).

## The three pillars

### 1. Triangulation: data × persona × coverage

Every claimed gap gets a confidence score:

```
confidence(gap) = α · data_frequency           # ∝ HN/Reddit/G2/X mentions
                + β · persona_agreement        # ∝ how many personas independently vote
                - γ · existing_coverage        # − coverage by existing products
```

Why all three:
- **Data alone** = quote-mining, no decision frame. ("Users complain about X" — but would they pay?)
- **Personas alone** = invented preferences. (LLM hallucinates problems.)
- **Coverage analysis alone** = "no one's done Y" — but maybe no one wants Y.
- **All three** = real PMF signal.

### 2. Actionable output

Each gap surfaces a brief, not a paragraph:

```
GAP: <one-line description>
ICP: <segment + day-in-the-life>
PRICING ANCHOR: $X-Y/mo (justified by competitor Z's pricing)
TAM ESTIMATE: <existing-market × hypothesized-share>
EXISTENTIAL RISK: <which big-co could absorb this as a feature, when>
6-MONTH ROADMAP BRIEF: <3 milestones a solo founder could hit>
CONFIDENCE: <0-1, breakdown of data/persona/coverage weights>
```

Founders consume this directly. VC researchers consume this directly. Corp innovation teams consume this directly.

### 3. Calibration as moat

The unique asset that compounds over time:

> Every gap personalab identifies is a public prediction. Six months later, check the market — did someone fill that gap? Did a startup raise money in that space? Did the gap close? Compare to predictions personalab labeled "low confidence" — did they stay open?
>
> Publish prediction accuracy quarterly. After 4 quarters, "personalab's track record" becomes a quotable data asset no clone can replicate without time.

This is **the moat that survives Anthropic / OpenAI shipping a built-in feature**: they can replicate the prompt structure, but not the multi-year prediction track record.

## Architecture

### New abstractions

**`MarketAdapter`** (new ABC, parallel to `ProductAdapter`):

```python
class MarketAdapter(ABC):
    name: str  # e.g. "user-research-tools", "scheduling-saas"

    @abstractmethod
    def load_products(self) -> list[ProductSnapshot]:
        """List of existing products in this market, each with public-surface data."""

    @abstractmethod
    def load_signals(self) -> list[Signal]:
        """Public dissatisfaction quotes: HN comments, Reddit, G2, X."""

    @abstractmethod
    def market_definition(self) -> str:
        """Markdown describing the market (TAM, segments, buying triggers)."""
```

**`ProductSnapshot`**:
```python
@dataclass
class ProductSnapshot:
    name: str
    url: str
    pricing: list[PricingTier]
    features: list[str]
    public_description: str
    last_updated: str  # ISO date
```

**`Signal`**:
```python
@dataclass
class Signal:
    source: Literal["hn", "reddit", "g2", "x", "indiehackers", "github_issue"]
    url: str
    timestamp: float
    excerpt: str
    sentiment: float  # -1 to +1, optional
    tags: list[str]  # e.g. ["pricing", "missing_feature:X", "competitor_compare"]
```

**`MarketGapMode`** (new `TestMode`):

```python
class MarketGapMode(TestMode):
    """For each persona, identify their unmet needs given the market state."""

    async def run(self, personas, market: MarketAdapter, llm, config):
        # 1. Load market context (products + signals + definition)
        # 2. For each persona, prompt:
        #    "Given this market, what need would you personally pay for that
        #     no existing product fills? Be specific. Cite a signal or
        #     competitor that comes close."
        # 3. Cluster persona responses into candidate gaps
        # 4. For each candidate gap, compute confidence score
        # 5. Return ranked gap list with attributable persona quotes
```

**`GapReporter`** (new `Reporter`):

```python
class GapReporter(Reporter):
    """Render ranked gaps as actionable briefs."""
```

### Data ingestion (out-of-band but bundled)

`personalab fetch-market <market-name>` CLI subcommand:

- Reads `markets/<market-name>.yaml` (curated list of competitors + search queries)
- Fetches public product pages via `httpx`
- Fetches HN/Reddit/X via their search APIs (rate-limited, cached)
- Compiles into `MarketAdapter`-consumable JSON

This is a separate pipeline from `personalab run`. Cached results live in `~/.personalab/markets/<name>/snapshot-<date>.json`. The framework lets you "freeze" a market snapshot for reproducibility.

### Bootstrapping vs cold start

First markets to ship:
1. **AI user-research tools** (we're in this one, perfect dogfood)
2. **Scheduling SaaS** (Calendly + Cal.com + SavvyCal + ... + Microsoft Bookings + Google Appointments)
3. **Open-source DocuSign alternatives** (Documenso + DocSpring + alternatives)
4. **Internal-tool builders** (Retool + Tooljet + Appsmith + ...)
5. **Product analytics** (PostHog + Mixpanel + Amplitude + Heap + Plausible + ...)

Each takes ~4-6 hours to author the `<market>.yaml` + cached snapshot.

## Honest disclaimers (carried over)

- **Synthetic + public-source ≠ ground truth.** This is a hypothesis engine. Every gap personalab surfaces should drive a real customer-discovery conversation, not be trusted as PMF proof.
- **Privacy / scraping ethics.** Only public surfaces. No paywalled content, no logged-in scraping, full respect for rate limits and ToS. Pre-cached datasets distributed under appropriate licenses where applicable.
- **Persona authenticity.** Same contamination risk as case studies — fix via TODO-1 (separate user profile from product preference) before relying on `MarketGapMode` output for serious decisions.

## Implementation phases

| Phase | Deliverable | Time | Status |
|---|---|---|---|
| Phase 0 (now) | This vision document | done | ✅ |
| Phase 1 (M3) | `MarketAdapter` + `MarketGapMode` SDK only, mock data | ~10h | planned |
| Phase 2 (M3) | `personalab fetch-market` for 2 hand-curated markets | ~10h | planned |
| Phase 3 (M4) | `GapReporter` with confidence breakdown + actionable briefs | ~8h | planned |
| Phase 4 (M5) | First public market gap report (e.g. "What's missing in scheduling SaaS in May 2026?") | ~6h authoring | planned |
| Phase 5 (M6+) | Calibration tracker — recheck past predictions, publish accuracy | quarterly | long-term |

## Pricing model implications

This features changes the monetization shape:

- Current ($99-499/mo Team plan thesis): pays per evaluation of *their* product. Low frequency, plateau.
- With market-gap mode ($99-$499/mo individual / $1500-5000/mo team): pays for **monthly gap reports** in their target market. Recurring need. Plus paid bespoke reports ($2-5k each).

The bespoke-report business line might actually outperform the SaaS line — it sells consultancy time wrapped in a tool.

## Risks

1. **LLM-circular epistemics**: personalab uses LLM to find gaps that LLM-trained-data already saw. We might just be regurgitating public sentiment. (Counter: this is exactly why the calibration moat is needed — track which predictions actually came true.)
2. **Big-co absorption**: if YC partners or a16z PMs start using this internally, they could publish a comparable internal tool, killing the standalone value. (Counter: ship fast, build the calibration dataset, license it before commodity.)
3. **Quality at scale**: 12 personas × N markets × ongoing snapshots = lots of LLM calls. Need cheap-model defaults and aggressive caching. (Counter: design for Gemini Flash / Haiku price points by default.)

## Decision: build it?

**Yes, but staged**. Phase 1-3 (~28h) is justified by the new positioning alone. Phase 4 onward depends on whether Case Study #1 (PostHog) + #2 (Cal.com) generate traction.

If Show HN gets <100 upvotes and no inbound, *stop here* — keep personalab as a product-feedback OSS tool, don't chase the market-gap-finder pivot.

If Show HN clears 200 upvotes / 10 inbound / 1 acquihire-feeler, *go all in on Phase 4*. The thesis-engine positioning is the path to $100k+ ARR (vs $5-12k Acquire.com sale).
