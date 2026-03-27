"""Tracking and alert-rule logic for fiat and crypto markets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from api_handler import APIHandler

Direction = Literal["above", "below"]


@dataclass(slots=True)
class PriceAlert:
    """Represent a simple threshold alert rule."""

    asset_name: str
    threshold: float
    direction: Direction
    label: str


class MarketTracker:
    """Coordinate data retrieval and alert evaluation."""

    def __init__(self, api_handler: APIHandler) -> None:
        """
        Initialize tracker with an API dependency.

        Args:
            api_handler: A configured API handler instance.
        """
        self.api_handler = api_handler
        self.fx_alerts: list[PriceAlert] = []
        self.crypto_alerts: list[PriceAlert] = []

    def add_fx_alert(self, pair_label: str, threshold: float, direction: Direction) -> None:
        """
        Register a fiat currency alert rule.

        Args:
            pair_label: Label to display for this pair (e.g., 'USD/TRY').
            threshold: Numeric threshold value.
            direction: Trigger condition ('above' or 'below').
        """
        self.fx_alerts.append(
            PriceAlert(asset_name=pair_label, threshold=threshold, direction=direction, label=pair_label)
        )

    def add_crypto_alert(self, coin_id: str, threshold: float, direction: Direction) -> None:
        """
        Register a crypto alert rule.

        Args:
            coin_id: CoinGecko coin id (e.g., 'bitcoin').
            threshold: Numeric threshold value.
            direction: Trigger condition ('above' or 'below').
        """
        self.crypto_alerts.append(
            PriceAlert(asset_name=coin_id.lower(), threshold=threshold, direction=direction, label=coin_id.upper())
        )

    def get_fx_snapshot(self, base: str, targets: list[str]) -> dict[str, float]:
        """
        Retrieve latest fiat rates for selected targets.

        Args:
            base: Base fiat currency code.
            targets: Target fiat currency codes.

        Returns:
            Dictionary of target currency rates.
        """
        return self.api_handler.get_exchange_rates(base=base, targets=targets)

    def get_crypto_snapshot(self, coin_id: str, vs_currency: str = "usd") -> float:
        """
        Retrieve latest crypto quote for a single asset.

        Args:
            coin_id: CoinGecko coin id.
            vs_currency: Quote currency code.

        Returns:
            Current price for the requested crypto asset.
        """
        return self.api_handler.get_crypto_price(coin_id=coin_id, vs_currency=vs_currency)

    def evaluate_alert(self, current_price: float, alert: PriceAlert) -> bool:
        """
        Check if one alert is triggered by current price.

        Args:
            current_price: Current market price.
            alert: Alert rule definition.

        Returns:
            True if alert is triggered, otherwise False.
        """
        if alert.direction == "above":
            return current_price > alert.threshold
        return current_price < alert.threshold

    def check_fx_alerts(self, rates: dict[str, float], base: str) -> list[str]:
        """
        Evaluate all fiat alerts against current rates.

        Args:
            rates: Dictionary of current rates by target code.
            base: Base fiat currency code used for this snapshot.

        Returns:
            Human-readable messages for triggered alerts.
        """
        messages: list[str] = []
        for alert in self.fx_alerts:
            _, target = alert.asset_name.split("/")
            target_code = target.upper()
            if target_code not in rates:
                continue
            price = rates[target_code]
            if self.evaluate_alert(current_price=price, alert=alert):
                messages.append(
                    f"[ALERT] {base.upper()}/{target_code} is {price:.4f} and moved {alert.direction} {alert.threshold:.4f}."
                )
        return messages

    def check_crypto_alerts(self, current_prices: dict[str, float], vs_currency: str) -> list[str]:
        """
        Evaluate all crypto alerts against current quotes.

        Args:
            current_prices: Mapping of coin id to current price.
            vs_currency: Quote currency for formatting output.

        Returns:
            Human-readable messages for triggered alerts.
        """
        messages: list[str] = []
        for alert in self.crypto_alerts:
            if alert.asset_name not in current_prices:
                continue
            price = current_prices[alert.asset_name]
            if self.evaluate_alert(current_price=price, alert=alert):
                messages.append(
                    f"[ALERT] {alert.label} is {price:.2f} {vs_currency.upper()} and moved {alert.direction} {alert.threshold:.2f}."
                )
        return messages
