"""Offline unit tests: no Yahoo Finance request or OpenAI API key needed."""

import unittest

from agents.strategy_agent import assess_investment_strategy, format_strategy_assessment


class InvestmentStrategyTests(unittest.TestCase):
    def test_growth_and_favorable_outlooks(self):
        metrics = {
            "return_3m": 0.12, "return_1y": 0.24, "beta": 1.0,
            "profit_margin": 0.22, "revenue_growth": 0.18,
            "earnings_growth": 0.19, "debt_to_equity": 60,
            "pe_ratio": 42, "price_to_book": 8,
        }
        result = assess_investment_strategy(metrics)
        self.assertEqual(result["short_term"]["label"], "Favorable")
        self.assertEqual(result["long_term"]["label"], "Favorable")
        self.assertEqual(result["investment_style"]["label"], "Growth")

    def test_value_and_cautious_momentum(self):
        metrics = {
            "return_3m": -0.08, "return_1y": -0.14, "beta": 1.0,
            "profit_margin": 0.13, "revenue_growth": 0.01,
            "earnings_growth": 0.02, "debt_to_equity": 60,
            "pe_ratio": 13, "price_to_book": 2.2,
        }
        result = assess_investment_strategy(metrics)
        self.assertEqual(result["short_term"]["label"], "Cautious")
        self.assertEqual(result["investment_style"]["label"], "Value")

    def test_blend_classification(self):
        metrics = {
            "revenue_growth": 0.15, "earnings_growth": 0.12,
            "pe_ratio": 17, "price_to_book": 2.7,
        }
        result = assess_investment_strategy(metrics)
        self.assertEqual(result["investment_style"]["label"], "Blend")
        self.assertEqual(result["long_term"]["label"], "Insufficient Data")

    def test_missing_fields_do_not_create_false_certainty(self):
        result = assess_investment_strategy({"pe_ratio": "N/A"})
        self.assertEqual(result["short_term"]["label"], "Insufficient Data")
        self.assertEqual(result["long_term"]["label"], "Insufficient Data")
        self.assertEqual(result["investment_style"]["label"], "Insufficient Data")
        self.assertIn("Short-Term", format_strategy_assessment(result))

    def test_high_beta_changes_momentum_label_to_mixed(self):
        result = assess_investment_strategy({
            "return_3m": 0.11, "return_1y": 0.22, "beta": 2.0
        })
        self.assertEqual(result["short_term"]["label"], "Mixed")


if __name__ == "__main__":
    unittest.main()
