# FinAgent an AI-Powered Financial Research Assistant

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

## Testing and Evaluation

### Unit Tests

Five automated unit tests cover growth, value, blend, missing-data, and high-beta scenarios. All five pass, and they run without an OpenAI API key (see Installation and Usage).

### Strategy Comparison: AAPL, NVDA, and JPM

We ran the strategy assessment on Yahoo Finance data for three companies (Colab run, October 19, 2026):

| Stock | 3-Month Return | Short-Term Outlook | Long-Term Outlook | Investment Style |
|---|---|---|---|---|
| Apple (`AAPL`) | 4.7% | Mixed | Favorable | Growth |
| NVIDIA (`NVDA`) | 4.8% | Mixed | Favorable | Growth |
| JPMorgan Chase (`JPM`) | -2.9% | Mixed | Favorable | Blend |

*These results reflect market data at the time of the run and are not live recommendations. Market data and classifications change over time.*

Key observations:

- **Long-term:** All three companies were Favorable, with profit margins ranging from 27.6% (AAPL) to 63.7% (NVDA). Yahoo Finance did not report a debt-to-equity ratio for JPM, so its long-term label was based on two of the three metrics, which the rule allows.
- **Short-term:** All three were Mixed. AAPL and NVDA had 3-month returns just under the 5% threshold, and NVDA's beta (2.22) would also lower its label. In an earlier run, AAPL's 3-month return was 5.3% and its short-term outlook was Favorable, which shows how sensitive fixed thresholds are to small market movements.
- **Investment style:** AAPL and NVDA were classified as Growth (high growth and high valuations, with trailing P/E ratios of 39.33 and 27.45). JPM was a Blend: its 10.2% revenue growth met the growth threshold, and its P/E (13.99) and price-to-book (2.52) met the value thresholds.

The comparisons show that the rules can distinguish financial characteristics across companies. However, the assessments are educational screening indicators, **not forecasts of future returns**. Applying the same thresholds to every sector is a limitation; sector-relative comparisons would make the labels more meaningful.

### Generative AI Integration Testing

The complete FinAgent workflow was tested using Apple (AAPL). The application retrieved Apple's 10-K filing, extracted the Risk Factors section and split it into 141 text chunks, scored the first 20 chunks with FinBERT, collected financial metrics from Yahoo Finance, and generated a structured investment brief with GPT-4o-mini.

The generated brief incorporated:

- Short-term investment outlook (0–12 months)
- Long-term investment outlook (3–5 years)
- Growth versus value classification
- Supporting financial metrics and explanations

Running the workflow more than once surfaced important limitations of generative AI:

- **Inconsistent rule application:** In one run, GPT-4o-mini recommended **Buy** even though Apple's P/E ratio (39.39) did not meet the prompt's requirement of a P/E below 30 for a Buy rating. Another run applied the rule correctly. The same prompt can produce different conclusions.
- **Sentiment interpretation:** The model treated FinBERT's negative sentiment score as a market concern, but risk disclosures are written in negative language by design, so negative sentiment there does not necessarily signal negative overall market sentiment.

These results highlight the importance of human oversight when evaluating generative AI outputs.

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
- Ramon Gonzalez
- Brianna Sanchez
