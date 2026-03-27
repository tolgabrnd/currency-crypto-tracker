"""Unit tests for tracker module."""

from __future__ import annotations

import unittest

from api_handler import APIHandler
from tracker import MarketTracker, PriceAlert


class TestMarketTracker(unittest.TestCase):
    """Test alert logic in MarketTracker."""

    def setUp(self) -> None:
        """Create a tracker instance with default API handler."""
        self.tracker = MarketTracker(api_handler=APIHandler())

    def test_evaluate_alert_above_returns_true(self) -> None:
        """Return True when current price is above threshold."""
        alert = PriceAlert(asset_name="USD/TRY", threshold=30.0, direction="above", label="USD/TRY")
        self.assertTrue(self.tracker.evaluate_alert(current_price=31.2, alert=alert))

    def test_evaluate_alert_below_returns_true(self) -> None:
        """Return True when current price is below threshold."""
        alert = PriceAlert(asset_name="bitcoin", threshold=70000.0, direction="below", label="BTC")
        self.assertTrue(self.tracker.evaluate_alert(current_price=65000.0, alert=alert))

    def test_check_fx_alerts_returns_message_when_triggered(self) -> None:
        """Produce alert message for triggered forex rule."""
        self.tracker.add_fx_alert(pair_label="USD/TRY", threshold=30.0, direction="above")
        messages = self.tracker.check_fx_alerts(rates={"TRY": 31.0}, base="USD")
        self.assertEqual(len(messages), 1)
        self.assertIn("[ALERT]", messages[0])
        self.assertIn("USD/TRY", messages[0])

    def test_check_crypto_alerts_returns_empty_when_not_triggered(self) -> None:
        """Return empty result when no crypto alerts are triggered."""
        self.tracker.add_crypto_alert(coin_id="bitcoin", threshold=10000.0, direction="below")
        messages = self.tracker.check_crypto_alerts(current_prices={"bitcoin": 45000.0}, vs_currency="usd")
        self.assertEqual(messages, [])


if __name__ == "__main__":
    unittest.main()
