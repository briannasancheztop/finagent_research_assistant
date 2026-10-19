
# FinAgent — AI-Powered Financial Research Assistant

FinAgent is a Python-based financial research application that combines SEC filings, financial sentiment analysis, market data, and generative AI to produce structured investment research briefs.

**GitHub:** https://github.com/briannasancheztop/finagent_research_assistant  
**Course Project:** Option 2 — Generative AI Application

## Project Overview

Financial research involves reviewing lengthy corporate filings and interpreting financial indicators from different sources. FinAgent brings these tasks together in one workflow, combining traditional data analytics with OpenAI's GPT-4o-mini API to summarize evidence and explain investment considerations.

## Features

- **SEC filing analysis:** Downloads a company's available 10-K filing and extracts text from its Risk Factors section.
- **Financial sentiment analysis:** Uses FinBERT (ProsusAI) to classify risk-related text as positive, negative, or neutral.
- **Market data:** Retrieves stock price, market capitalization, valuation ratios, profitability, growth metrics, beta, and historical price returns through Yahoo Finance.
- **Investment strategy assessment:** Uses transparent, rule-based metrics to classify short-term outlook (0–12 months), long-term outlook (3–5 years), and investment style (Growth, Value, Blend, or Unclear).
- **Generative AI report:** Sends the financial data, sentiment analysis, and strategy assessments to GPT-4o-mini to produce an investment research brief with supporting explanations.

## Technologies

| Technology | Role |
|---|---|
| Python | Data processing and application logic |
| SEC EDGAR | Corporate 10-K filings |
| FinBERT, Transformers, PyTorch | Financial text sentiment analysis |
| Yahoo Finance (`yfinance`) | Market data and historical returns |
| OpenAI API (`gpt-4o-mini`) | Investment brief generation |

## How It Works

1. The user enters a stock ticker, such as `AAPL`.
2. FinAgent retrieves an SEC 10-K filing and extracts risk-related text.
3. FinBERT analyzes the filing's risk sentiment while Yahoo Finance supplies financial metrics.
4. Python-based rules assess historical momentum, long-term fundamental indicators, and growth/value characteristics.
5. GPT-4o-mini synthesizes these results into an educational investment research brief.

## Preliminary Testing and Evaluation

We ran five automated tests covering growth, value, blend, missing-data handling, and high-beta scenarios. We also tested the strategy assessment with Yahoo Finance data for three companies:

| Stock | Short-Term Outlook | Long-Term Outlook | Investment Style |
|---|---|---|---|
| Apple (`AAPL`) | Favorable | Favorable | Growth |
| NVIDIA (`NVDA`) | Mixed | Favorable | Growth |
| JPMorgan Chase (`JPM`) | Mixed | Favorable | Blend |

*These are preliminary results from the October 2026 testing session, not live recommendations. Market data and classifications may change.*

The comparisons show that the rules can distinguish some financial characteristics across companies. However, the assessments are educational screening indicators, **not forecasts of future returns**. Broad valuation thresholds may be less informative across different sectors, and favorable fundamental signals do not guarantee investment success. AI-generated explanations may also contain errors and require verification.

### Generative AI Integration Testing

The complete FinAgent workflow was successfully tested
using Apple (AAPL).

The application retrieved SEC filing data, processed
141 text chunks through FinBERT, collected financial
metrics from Yahoo Finance, and generated a structured
investment brief using GPT-4o-mini.

The generated report successfully incorporated:

- Short-term investment outlook (0–12 months)
- Long-term investment outlook (3–5 years)
- Growth versus value classification
- Supporting financial metrics and explanations

The test confirmed that the Python-based investment
classifications were incorporated into the
AI-generated report.

A key limitation identified was that negative sentiment
in corporate risk disclosures can be misinterpreted as
negative overall market sentiment. This highlights
the importance of human oversight when evaluating
generative AI outputs.


## Installation and Usage

**Prerequisites:** Python 3.10+, Git, internet access, and an OpenAI API key for full report generation.

1. Clone the repository and check out the strategy development branch:

   ```bash
   git clone https://github.com/briannasancheztop/finagent_research_assistant.git
   cd finagent_research_assistant
   git checkout Investment-strategy
   ```

2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Create a `.env` file in the project folder with:

   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

   Never commit your `.env` file or share API keys publicly.

4. Run the application and enter a stock ticker when prompted:

   ```bash
   python main.py
   ```

To run the strategy tests **without an OpenAI API key**:

```bash
python -m unittest discover -s tests -v
```

## Limitations and Responsible Use

The accuracy of FinAgent depends on the quality and availability of SEC filings and Yahoo Finance data. FinBERT sentiment does not directly measure stock performance, and rules based on historical prices or accounting metrics cannot predict future returns. The SEC risk-text extraction and AI-generated narrative should be reviewed for accuracy before relying on any findings.

**Disclaimer:** FinAgent is for educational and research purposes only. It does not provide personalized investment advice.

## Project Team

- Faye Corprew
- Ramon Dario
- Brianna Sanchez
