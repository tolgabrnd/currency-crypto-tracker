"""Unit tests for API handler module."""

from __future__ import annotations

import unittest

from api_handler import APIHandler, APIHandlerError


class TestAPIHandler(unittest.TestCase):
    """Test API payload parsing without making network calls."""

    def setUp(self) -> None:
        """Create API handler instance."""
        self.handler = APIHandler()

    def test_get_exchange_rates_success(self) -> None:
        """Parse rates from expected payload schema."""
        self.handler._get_json = lambda url, params=None: {"rates": {"TRY": 39.1, "EUR": 0.92}}  # type: ignore[method-assign]
        result = self.handler.get_exchange_rates(base="USD", targets=["TRY", "EUR"])
        self.assertEqual(result, {"TRY": 39.1, "EUR": 0.92})

    def test_get_exchange_rates_raises_for_missing_rates(self) -> None:
        """Raise APIHandlerError when rates key is missing."""
        self.handler._get_json = lambda url, params=None: {"unexpected": "payload"}  # type: ignore[method-assign]
        with self.assertRaises(APIHandlerError):
            self.handler.get_exchange_rates(base="USD", targets=["TRY"])

    def test_get_crypto_price_success(self) -> None:
        """Parse crypto value from expected payload schema."""
        self.handler._get_json = lambda url, params=None: {"bitcoin": {"usd": 65234.0}}  # type: ignore[method-assign]
        result = self.handler.get_crypto_price(coin_id="bitcoin", vs_currency="usd")
        self.assertEqual(result, 65234.0)

    def test_get_crypto_price_raises_for_invalid_coin(self) -> None:
        """Raise APIHandlerError when coin payload is unavailable."""
        self.handler._get_json = lambda url, params=None: {"ethereum": {"usd": 3500.0}}  # type: ignore[method-assign]
        with self.assertRaises(APIHandlerError):
            self.handler.get_crypto_price(coin_id="bitcoin", vs_currency="usd")


if __name__ == "__main__":
    unittest.main()
