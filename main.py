import os
import sys
from dotenv import load_dotenv
from sec_edgar_downloader import Downloader
from agents.research_agent import generate_investment_brief

load_dotenv()

def download_10k(ticker: str) -> str:
    filing_dir = f"data/sec-edgar-filings/{ticker}/10-K"

    if not os.path.exists(filing_dir) or not os.listdir(filing_dir):
        print(f"Downloading {ticker} 10-K from SEC EDGAR...")
        dl = Downloader("FinAgent", "ramondario1216@gmail.com", "data")
        dl.get("10-K", ticker, limit=1)
    else:
        print(f"Using cached 10-K for {ticker}")

    if not os.path.exists(filing_dir) or not os.listdir(filing_dir):
        return None

    filing_path = os.path.join(filing_dir, os.listdir(filing_dir)[0])

    for file in os.listdir(filing_path):
        if file.endswith(".txt") or file.endswith(".htm"):
            return os.path.join(filing_path, file)

    return None

if __name__ == "__main__":
    ticker = input("Enter a stock ticker: ").upper().strip()

    if not ticker:
        print("No ticker entered.")
        sys.exit(1)

    filing_path = download_10k(ticker)

    if filing_path is None:
        print(f"Could not find a 10-K for {ticker}")
        sys.exit(1)

    brief = generate_investment_brief(ticker, filing_path)

    print("\n" + "=" * 60)
    print(f"FINAGENT INVESTMENT BRIEF: {ticker}")
    print("=" * 60)
    print(brief)