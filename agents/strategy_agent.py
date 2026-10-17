"""Rule-based investment strategy signals for FinAgent.

Educational heuristics, not forecasts or personalized investment advice.
Yahoo Finance growth and return fields are decimal fractions (0.10 = 10%).
Yahoo Finance debtToEquity is normally expressed as a percentage (100 = 1x).
"""

import math
from typing import Any


def _number(value: Any) -> float | None:
    """Return a finite number or None for unavailable / invalid metrics."""
    if isinstance(value, bool) or value in (None, "", "N/A"):
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _pct(value: Any) -> str:
    amount = _number(value)
    return "N/A" if amount is None else f"{amount * 100:.1f}%"


def assess_investment_strategy(data: dict) -> dict:
    """Assess historical momentum, fundamentals, and growth/value signals.

    Outputs descriptive labels only. These thresholds are illustrative,
    not empirically validated investment recommendations.
    """
    r3 = _number(data.get("return_3m"))
    r1 = _number(data.get("return_1y"))
    beta = _number(data.get("beta"))
    margin = _number(data.get("profit_margin"))
    revenue_growth = _number(data.get("revenue_growth"))
    earnings_growth = _number(data.get("earnings_growth"))
    debt = _number(data.get("debt_to_equity"))
    trailing_pe = _number(data.get("pe_ratio"))
    price_to_book = _number(data.get("price_to_book"))

    # SHORT-TERM: Describe recent price movement; do not predict future returns.
    if r3 is None or r1 is None:
        short_term = "Insufficient Data"
    elif r3 >= 0.05 and r1 > 0:
        short_term = "Favorable"
        if beta is not None and beta > 1.5:
            short_term = "Mixed"  # strong momentum, but relatively high beta
    elif r3 <= -0.05 and r1 < 0:
        short_term = "Cautious"
    else:
        short_term = "Mixed"

    short_reason = (
        f"3-month historical return: {_pct(r3)}; "
        f"1-year historical return: {_pct(r1)}; "
        f"beta: {f'{beta:.2f}' if beta is not None else 'N/A'}. "
        "Historical momentum and beta cannot predict future returns."
    )

    # LONG-TERM: Compare illustrative fundamental signals; require >=2 metrics.
    available = sum(v is not None for v in (margin, revenue_growth, debt))
    favorable = sum((
        margin is not None and margin >= 0.10,
        revenue_growth is not None and revenue_growth >= 0.05,
        debt is not None and debt <= 100,
    ))
    concerning = sum((
        margin is not None and margin < 0,
        revenue_growth is not None and revenue_growth <= -0.05,
        debt is not None and debt > 200,
    ))
    if available < 2:
        long_term = "Insufficient Data"
    elif favorable >= 2 and concerning == 0:
        long_term = "Favorable"
    elif concerning >= 2 and favorable == 0:
        long_term = "Cautious"
    else:
        long_term = "Mixed"

    long_reason = (
        f"profit margin: {_pct(margin)}; "
        f"revenue growth: {_pct(revenue_growth)}; "
        f"debt/equity (Yahoo Finance percentage convention): "
        f"{f'{debt:.1f}' if debt is not None else 'N/A'}. "
        "These are screening indicators, not a 3-5 year return forecast."
    )

    # INVESTMENT STYLE: Growth and value are descriptive *characteristics*,
    # ideally interpreted relative to peers within the same industry.
    growth_available = sum(v is not None for v in (revenue_growth, earnings_growth))
    value_available = sum(v is not None for v in (trailing_pe, price_to_book))
    growth_signals = sum((
        revenue_growth is not None and revenue_growth >= 0.10,
        earnings_growth is not None and earnings_growth >= 0.10,
    ))
    value_signals = sum((
        trailing_pe is not None and 0 < trailing_pe <= 20,
        price_to_book is not None and 0 < price_to_book <= 3,
    ))
    if not growth_available or not value_available:
        style = "Insufficient Data"
    elif growth_signals and value_signals:
        style = "Blend"
    elif growth_signals:
        style = "Growth"
    elif value_signals:
        style = "Value"
    else:
        style = "Unclear"

    style_reason = (
        f"revenue growth: {_pct(revenue_growth)}; "
        f"earnings growth: {_pct(earnings_growth)}; "
        f"trailing P/E: {f'{trailing_pe:.2f}' if trailing_pe is not None else 'N/A'}; "
        f"price/book: {f'{price_to_book:.2f}' if price_to_book is not None else 'N/A'}. "
        "Simple absolute thresholds are illustrative; sector-relative comparisons "
        "would improve this classification."
    )

    return {
        "short_term": {"label": short_term, "evidence": short_reason},
        "long_term": {"label": long_term, "evidence": long_reason},
        "investment_style": {"label": style, "evidence": style_reason},
    }


def format_strategy_assessment(result: dict) -> str:
    """Format rules and supporting metrics for the language-model prompt."""
    return "\n".join(
        f"{heading}: {result[key]['label']}\nEvidence: {result[key]['evidence']}"
        for heading, key in (
            ("Short-Term (0-12 months)", "short_term"),
            ("Long-Term (3-5 years)", "long_term"),
            ("Investment Style (Growth/Value)", "investment_style"),
        )
    )
