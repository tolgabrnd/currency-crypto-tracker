"""Application entry point for market tracking."""

from __future__ import annotations

import requests

from api_handler import APIHandler, APIHandlerError
from tracker import Direction, MarketTracker


def ask_direction(prompt: str) -> Direction:
    """
    Ask the user for a valid alert direction.

    Args:
        prompt: Input prompt shown to the user.

    Returns:
        A validated direction literal: 'above' or 'below'.
    """
    while True:
        value = input(prompt).strip().lower()
        if value in {"above", "below"}:
            return value
        print("Please type only 'above' or 'below'.")


def ask_float(prompt: str) -> float:
    """
    Ask the user for a numeric threshold value.

    Args:
        prompt: Input prompt shown to the user.

    Returns:
        Parsed float value.
    """
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Invalid number. Please try again (example: 42.5).")


def run() -> None:
    """
    Start a simple CLI workflow for fiat and crypto tracking.

    The function gathers user inputs, fetches current market data,
    prints snapshots, and evaluates optional alert rules.
    """
    print("=== Currency and Crypto Tracker ===")

    base = input("Enter base currency code (example: USD): ").strip().upper() or "USD"
    targets_text = input("Enter target currency codes separated by commas (example: TRY,EUR): ").strip()
    coin_id = input("Enter crypto coin id to track (example: bitcoin): ").strip().lower() or "bitcoin"
    vs_currency = input("Enter quote currency for crypto price (example: usd): ").strip().lower() or "usd"

    targets = [item.strip().upper() for item in targets_text.split(",") if item.strip()]
    if not targets:
        targets = ["TRY"]

    api_handler = APIHandler()
    tracker = MarketTracker(api_handler=api_handler)

    try:
        rates = tracker.get_fx_snapshot(base=base, targets=targets)
        crypto_price = tracker.get_crypto_snapshot(coin_id=coin_id, vs_currency=vs_currency)
    except APIHandlerError as exc:
        print(f"An error occurred while fetching data: {exc}")
        return
    except requests.RequestException as exc:
        print(f"Network or API connection error: {exc}")
        return
    except ValueError as exc:
        print(f"Data conversion error in API response: {exc}")
        return

    print("\n--- Live Snapshot ---")
    for target_code, rate in rates.items():
        print(f"{base}/{target_code}: {rate:.4f}")
    print(f"{coin_id.upper()}/{vs_currency.upper()}: {crypto_price:.2f}")

    print("\n--- Alert Rules (Optional) ---")
    add_fx = input("Would you like to add a forex alert? (y/n): ").strip().lower()
    if add_fx == "y":
        fx_pair = f"{base}/{targets[0]}"
        fx_direction = ask_direction("Alert direction ('above' or 'below'): ")
        fx_threshold = ask_float("Enter threshold value: ")
        tracker.add_fx_alert(pair_label=fx_pair, threshold=fx_threshold, direction=fx_direction)

    add_crypto = input("Would you like to add a crypto alert? (y/n): ").strip().lower()
    if add_crypto == "y":
        crypto_direction = ask_direction("Alert direction ('above' or 'below'): ")
        crypto_threshold = ask_float("Enter threshold value: ")
        tracker.add_crypto_alert(coin_id=coin_id, threshold=crypto_threshold, direction=crypto_direction)

    fx_alert_messages = tracker.check_fx_alerts(rates=rates, base=base)
    crypto_alert_messages = tracker.check_crypto_alerts(
        current_prices={coin_id: crypto_price},
        vs_currency=vs_currency,
    )

    print("\n--- Alert Results ---")
    if not fx_alert_messages and not crypto_alert_messages:
        print("No alerts were triggered.")
        return

    for message in fx_alert_messages + crypto_alert_messages:
        print(message)


if __name__ == "__main__":
    run()
