"""API client utilities for currency and crypto price retrieval."""

from __future__ import annotations

from typing import Any

import requests


class APIHandlerError(Exception):
    """Represent user-friendly API integration errors."""


class APIHandler:
    """Handle HTTP requests to market data endpoints."""

    def __init__(self, timeout: float = 10.0) -> None:
        """
        Initialize the API handler.

        Args:
            timeout: Maximum number of seconds to wait for HTTP responses.
        """
        self.timeout = timeout

    def _get_json(self, url: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        """
        Send a GET request and return parsed JSON payload.

        Args:
            url: Full endpoint URL.
            params: Optional query parameters.

        Returns:
            Parsed JSON response body.

        Raises:
            requests.RequestException: If the request fails or status is not successful.
            ValueError: If the response payload is not valid JSON.
        """
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_exchange_rates(self, base: str, targets: list[str]) -> dict[str, float]:
        """
        Fetch exchange rates for a base currency against target currencies.

        Args:
            base: Base fiat currency code (e.g., 'USD').
            targets: List of target fiat codes (e.g., ['TRY', 'EUR']).

        Returns:
            A mapping where keys are target currency codes and values are rates.

        Raises:
            requests.RequestException: If the API call fails.
            APIHandlerError: If the API payload format is unexpected.
        """
        url = "https://api.frankfurter.app/latest"
        params = {"from": base.upper(), "to": ",".join(code.upper() for code in targets)}
        payload = self._get_json(url, params=params)

        rates_obj = payload.get("rates")
        if not isinstance(rates_obj, dict):
            raise APIHandlerError(
                "Exchange-rate data did not arrive in the expected format. Please verify currency codes (example: USD, TRY, EUR)."
            )

        result: dict[str, float] = {}
        for code in targets:
            normalized_code = code.upper()
            if normalized_code not in rates_obj:
                raise APIHandlerError(
                    f"No exchange-rate data found for '{normalized_code}'. Please enter a valid currency code."
                )
            result[normalized_code] = float(rates_obj[normalized_code])
        return result

    def get_crypto_price(self, coin_id: str, vs_currency: str = "usd") -> float:
        """
        Fetch current crypto price from CoinGecko.

        Args:
            coin_id: CoinGecko coin id (e.g., 'bitcoin', 'ethereum').
            vs_currency: Fiat quote currency code (e.g., 'usd', 'try').

        Returns:
            Current coin price in the selected quote currency.

        Raises:
            requests.RequestException: If the API call fails.
            APIHandlerError: If the API payload format is unexpected.
        """
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": coin_id.lower(), "vs_currencies": vs_currency.lower()}
        payload = self._get_json(url, params=params)

        coin_payload = payload.get(coin_id.lower())
        if not isinstance(coin_payload, dict) or vs_currency.lower() not in coin_payload:
            raise APIHandlerError(
                "Crypto data was not found. Please enter a valid coin id (example: bitcoin, ethereum)."
            )
        return float(coin_payload[vs_currency.lower()])
