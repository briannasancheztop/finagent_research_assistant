from openai import OpenAI
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.market_agent import get_market_data, format_market_data
from agents.sentiment_agent import analyze_sentiment
from utils.parser import extract_risk_factors

from pathlib import Path
load_dotenv(Path(__file__).parent.parent / ".env")

client = OpenAI()

def generate_investment_brief(ticker: str, filing_path: str) -> str:
    """Generates a full investment brief for a Financial Advisor."""
    
    print(f"\nGenerating investment brief for {ticker}...")
    
    # Step 1: Get market data
    print("Step 1/3: Fetching market data...")
    market_data = get_market_data(ticker)
    market_summary = format_market_data(market_data)
    
    # Step 2: Extract and analyze risk factors
    print("Step 2/3: Analyzing risk factors...")
    risk_text = extract_risk_factors(filing_path)
    sentiment = analyze_sentiment(risk_text)
    
    # Step 3: Synthesize with LLM
    print("Step 3/3: Generating investment brief...")
    
    prompt = f"""
You are a financial analyst at a wealth management firm preparing a briefing for a Financial Advisor and their client.

Using the following data, generate a concise, professional investment brief that includes:
1. A quick disclosure that this is not financial advice, but a research summary.
2. Company Snapshot
3. Key Risk Assessment (based on the 10-K Risk Factors sentiment analysis)
4. Market Position
5. Investment Considerations for a wealth management client
6. Overall Recommendation: choose Buy, Hold, or Avoid using these rules:
   - Buy: profit margin above 15%, P/E below 30, and analyst rating of buy or strong_buy.
   - Avoid: negative profit margin, or debt/equity above 200, or analyst rating of sell or underperform.
   - Hold: only if neither Buy nor Avoid applies.
   State which rule you applied and justify it using only the data above.

MARKET DATA:
{market_summary}

RISK FACTORS SENTIMENT ANALYSIS (FinBERT):
Overall Sentiment: {sentiment['overall'].upper()}
Positive Score: {sentiment['scores']['positive']}
Negative Score: {sentiment['scores']['negative']}
Neutral Score:  {sentiment['scores']['neutral']}
Chunks Analyzed: {sentiment['chunks_analyzed']}

Write in a professional but accessible tone suitable for a Financial Advisor presenting to a client.
Keep the brief under 500 words.
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a senior financial analyst at a wealth management firm."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    ticker = "AAPL"
    filing_path = "data/sec-edgar-filings/AAPL/10-K/0000320193-25-000079/full-submission.txt"
    brief = generate_investment_brief(ticker, filing_path)
    print("\n" + "="*60)
    print("FINAGENT INVESTMENT BRIEF")
    print("="*60)
    print(brief)