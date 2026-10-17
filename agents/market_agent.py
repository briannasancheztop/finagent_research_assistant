import yfinance as yf


def _historical_returns(stock) -> tuple[float | None, float | None]:
    """Approx 3-month / 1-year price returns, from daily adjusted closes.
    backward-looking historical performance NOT a return prediction
    """
    try:
        prices = stock.history(period="1y", auto_adjust=True)["Close"].dropna()
        if len(prices) == 0 or float(prices.iloc[-1]) <= 0:
            return None, None
        three_month = None
        one_year = None
        if len(prices) >= 64 and float(prices.iloc[-64]) > 0:
            three_month = float(prices.iloc[-1] / prices.iloc[-64] - 1)
        if len(prices) >= 200 and float(prices.iloc[0]) > 0:
            one_year = float(prices.iloc[-1] / prices.iloc[0] - 1)
        return three_month, one_year
    except (KeyError, IndexError, TypeError, ValueError, AttributeError) as exc:
        print(f"Historical performance unavailable: {exc}")
        return None, None
    except Exception as exc:
        # data providers may fail / throttle.. don't fail the whole report.
        print(f"Could not retrieve historical market data: {exc}")
        return None, None


def get_market_data(ticker: str) -> dict:
    """market data and metrics for a given ticker."""
    print(f"Fetching market data for {ticker}...")
    stock = yf.Ticker(ticker)
    info = stock.info or {}
    return_3m, return_1y = _historical_returns(stock)
    summary = info.get("longBusinessSummary") or "N/A"

    return {
        "ticker": ticker,
        "company_name": info.get("longName", "N/A"),
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "price_to_book": info.get("priceToBook"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "revenue": info.get("totalRevenue"),
        "revenue_growth": info.get("revenueGrowth"),
        "earnings_growth": info.get("earningsGrowth"),
        "profit_margin": info.get("profitMargins"),
        "debt_to_equity": info.get("debtToEquity"),
        "beta": info.get("beta"),
        "return_3m": return_3m,
        "return_1y": return_1y,
        "analyst_rating": info.get("recommendationKey", "N/A"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "summary": summary[:500],
    }


def _currency(value):
    try:
        return f"${float(value):,.2f}" if value not in (None, "N/A") else "N/A"
    except (ValueError, TypeError):
        return "N/A"


def _percentage(value):
    try:
        return f"{float(value)*100:.1f}%" if value not in (None, "N/A") else "N/A"
    except (ValueError, TypeError):
        return "N/A"


def _large_currency(value):
    try:
        n = float(value)
    except (ValueError, TypeError):
        return "N/A"
    if n >= 1_000_000_000_000:
        return f"${n / 1_000_000_000_000:.2f}T"
    if n >= 1_000_000_000:
        return f"${n / 1_000_000_000:.2f}B"
    if n >= 1_000_000:
        return f"${n / 1_000_000:.2f}M"
    return f"${n:,.2f}"


def format_market_data(data: dict) -> str:
    """Format financial metrics as human readable evidence for GPT-4o-mini."""
    rating = data.get("analyst_rating") or "N/A"
    return f"""
MARKET DATA FOR {data['ticker']} - {data.get('company_name', 'N/A')}
Current Price: {_currency(data.get('current_price'))}
Market Cap: {_large_currency(data.get('market_cap'))}
P/E Ratio: {data.get('pe_ratio') or 'N/A'}
Forward P/E: {data.get('forward_pe') or 'N/A'}
Price-to-Book: {data.get('price_to_book') or 'N/A'}
52-Week High: {_currency(data.get('52_week_high'))}
52-Week Low: {_currency(data.get('52_week_low'))}
Revenue: {_large_currency(data.get('revenue'))}
Profit Margin: {_percentage(data.get('profit_margin'))}
Revenue Growth: {_percentage(data.get('revenue_growth'))}
Earnings Growth: {_percentage(data.get('earnings_growth'))}
Historical 3-Month Return: {_percentage(data.get('return_3m'))}
Historical 1-Year Return: {_percentage(data.get('return_1y'))}
Beta: {data.get('beta') if data.get('beta') is not None else 'N/A'}
Debt/Equity (Yahoo Finance percentage convention): {data.get('debt_to_equity') if data.get('debt_to_equity') is not None else 'N/A'}
Analyst Rating: {str(rating).upper()}
Sector: {data.get('sector') or 'N/A'}
Industry: {data.get('industry') or 'N/A'}
"""


if __name__ == "__main__":
    sample = get_market_data("AAPL")
    print(format_market_data(sample))
