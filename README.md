# FinAgent — AI-Powered Financial Research Assistant

FinAgent is an AI-powered financial research application that integrates natural language processing (NLP), financial market data, and generative AI to automate investment research and reporting.

The application uses SEC EDGAR filings, FinBERT sentiment analysis, Yahoo Finance, and OpenAI's GPT-4o-mini to generate structured investment briefs for publicly traded companies.

**GitHub Repository:** https://github.com/briannasancheztop/finagent_research_assistant

## Project Overview

Financial research often requires reviewing lengthy SEC filings, evaluating company risks, and interpreting financial metrics. FinAgent simplifies this process by automating data collection, sentiment analysis, and report generation.

This project demonstrates how generative AI can be integrated with traditional data science techniques to improve the efficiency and accessibility of financial research.

**Course Project:** Option 2 — Generative AI Application

## Project Objectives

- Automate financial data retrieval from SEC EDGAR and Yahoo Finance.
- Apply FinBERT to analyze sentiment within corporate risk disclosures.
- Integrate NLP results with quantitative financial indicators.
- Use OpenAI's GPT-4o-mini API to generate investment research briefs.
- Evaluate the effectiveness, reliability, and limitations of AI-generated financial insights.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development and data processing |
| OpenAI GPT-4o-mini | Generative AI report creation |
| FinBERT | Financial sentiment analysis |
| SEC EDGAR | Corporate 10-K filings |
| Yahoo Finance | Market data and financial metrics |
| LangChain | AI workflow orchestration |
| Streamlit | Interactive user interface |

## How FinAgent Works

1. **Ticker Input:** Users enter a publicly traded company's stock ticker.
2. **SEC Filing Retrieval:** FinAgent retrieves the company's latest available 10-K filing and extracts its Risk Factors section.
3. **Sentiment Analysis:** FinBERT classifies financial risk disclosures as positive, negative, or neutral.
4. **Market Data Collection:** Yahoo Finance provides financial indicators, including stock price, market capitalization, P/E ratio, and analyst recommendations.
5. **AI Report Generation:** GPT-4o-mini synthesizes the financial data and sentiment results into a structured investment brief.

The resulting report includes a company overview, financial snapshot, risk assessment, market position, and investment considerations.

## Generative AI Integration

FinAgent combines traditional financial analytics with generative AI.

FinBERT performs NLP-based sentiment classification, while Yahoo Finance supplies quantitative financial data. These analytical results are provided to GPT-4o-mini through the OpenAI API to generate readable financial interpretations.

This workflow demonstrates how large language models can complement traditional analytical methods by transforming structured data and unstructured financial text into accessible insights.

## Sample Output

**Company:** Apple Inc. (AAPL)

- Risk Sentiment: Negative (57.8%)
- Stock Price: $301.54
- Market Capitalization: $4.43T
- Analyst Recommendation: Buy

FinAgent uses these results to generate an investment brief summarizing company performance, financial risks, and investment considerations.

*Note: Figures are illustrative sample output and do not represent current market values.*

## Evaluation and Limitations

The effectiveness of FinAgent can be assessed through the accuracy, relevance, and consistency of its AI-generated investment reports.

The application demonstrates the potential of generative AI to streamline financial research by combining multiple data sources into a single report.

However, several limitations must be considered:

- **AI Accuracy:** Generated reports may contain unsupported conclusions or hallucinations.
- **Data Reliability:** Financial information may be delayed, incomplete, or outdated.
- **Sentiment Limitations:** Negative risk sentiment does not necessarily indicate poor financial performance.
- **Human Oversight:** AI-generated financial interpretations require verification before supporting investment decisions.

Generative AI is valuable for summarizing and interpreting financial information but should supplement, rather than replace, professional financial analysis.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/briannasancheztop/finagent_research_assistant.git
cd finagent_research_assistant
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure OpenAI API

Create a `.env` file in the project directory:

```env
OPENAI_API_KEY=your_api_key_here
```

Keep API credentials private and do not upload the `.env` file to GitHub.

### 5. Launch the Application

```bash
streamlit run app.py
```

Enter a stock ticker in the Streamlit interface to generate a financial research brief.

## Project Team

**Final Team Project — Option 2: Generative AI Application**

- Faye Corpew
- Ramon Dario
- Brianna Sanchez

## Disclaimer

FinAgent is intended for educational and research purposes only. AI-generated investment reports should not be considered professional financial advice. All financial information and recommendations should be independently verified.
