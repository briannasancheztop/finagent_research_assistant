import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.market_agent import format_market_data, get_market_data
from agents.sentiment_agent import analyze_sentiment
from agents.strategy_agent import assess_investment_strategy, format_strategy_assessment
from utils.parser import extract_risk_factors

load_dotenv(Path(__file__).parent.parent / ".env")
client = OpenAI()


def generate_investment_brief(ticker: str, filing_path: str) -> str:
    """generate an investment research brief with transparent strategy signals."""
    print(f"\nGenerating investment brief for {ticker}...")

    print("Step 1/3: Fetching market data and assessing investment style...")
    market_data = get_market_data(ticker)
    market_summary = format_market_data(market_data)
    strategy_summary = format_strategy_assessment(
        assess_investment_strategy(market_data)
    )

    print("Step 2/3: Analyzing risk factors...")
    risk_text = extract_risk_factors(filing_path)
    sentiment = analyze_sentiment(risk_text)

    print("Step 3/3: Generating investment brief...")
    prompt = f"""
You are a financial analyst preparing an educational investment research brief.
Use ONLY the financial data, sentiment scores, and rule-based assessment below.
If evidence is missing, say 'Insufficient Data' rather than inventing metrics.

Include these sections:
1. Disclosure: This is a research summary, not personalized financial advice.
2. Company Snapshot
3. Key Risk Assessment (interpret FinBERT sentiment carefully)
4. Market Position
5. Investment Considerations
6. Overall Recommendation: Buy, Hold, or Avoid, using these existing rules:
   - Avoid if profit margin is negative, debt/equity > 200 (Yahoo Finance
     percentage convention), or analyst rating is sell/underperform.
   - Otherwise Buy if profit margin > 15%, P/E < 30, and analyst rating
     is buy or strong_buy.
   - Otherwise Hold.
   - If essential inputs are missing, state that the rules cannot be fully
     assessed; do not assume missing data meet a rule.
   Explain which rules and evidence apply.
7. Short-Term Outlook (0-12 months): Present the provided short-term label
   and the historical momentum/volatility evidence. Do NOT predict returns.
8. Long-Term Outlook (3-5 years): Present the provided long-term label and
   fundamental evidence. Do NOT claim a 3-5 year return forecast.
9. Investment Style: Present the Growth / Value / Blend / Unclear label,
   its evidence, and note that sector-relative valuation could change it.

The three strategy labels are educational heuristics, not buy/sell signals.
They do not necessarily agree with the overall Buy/Hold/Avoid rule.
Be clear about uncertainty and limitations. Stay under 650 words.

MARKET DATA:
{market_summary}

RULE-BASED INVESTMENT STRATEGY ASSESSMENT:
{strategy_summary}

RISK FACTORS SENTIMENT ANALYSIS (FinBERT):
Overall Sentiment: {sentiment['overall'].upper()}
Positive Score: {sentiment['scores']['positive']}
Negative Score: {sentiment['scores']['negative']}
Neutral Score: {sentiment['scores']['neutral']}
Chunks Analyzed: {sentiment['chunks_analyzed']}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a careful financial research analyst. "
                "Never fabricate financial data or guarantee investment returns.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    ticker = "AAPL"
    filing_path = "data/sec-edgar-filings/AAPL/10-K/0000320193-25-000079/full-submission.txt"
    print(generate_investment_brief(ticker, filing_path))
