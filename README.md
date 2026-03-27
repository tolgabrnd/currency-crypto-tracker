# Currency and Crypto Tracker

A beginner-friendly Python CLI application that tracks live forex and cryptocurrency prices, then evaluates simple threshold alerts.

## Features

- Fetches forex rates for a base currency against selected targets
- Fetches a live crypto price by coin id
- Supports optional `above` / `below` threshold alerts
- Uses modular architecture (`api_handler`, `tracker`, `main`)
- Includes type hints, docstrings, and unit tests

## Project Structure

```text
project2/
├── api_handler.py
├── tracker.py
├── main.py
├── requirements.txt
├── tests/
│   ├── test_api_handler.py
│   └── test_tracker.py
└── .github/workflows/ci.yml
```

## APIs Used

- Forex: [Frankfurter](https://frankfurter.app/)
- Crypto: [CoinGecko API](https://www.coingecko.com/en/api)

## Requirements

- Python 3.11+
- Internet connection

## Installation

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Then install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Application

```bash
python main.py
```

## Run Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Example Usage

1. Enter base currency (for example: `USD`)
2. Enter target currencies (for example: `TRY,EUR`)
3. Enter coin id (for example: `bitcoin`)
4. Enter quote currency for crypto (for example: `usd`)
5. Optionally create alerts and view results

## Known Limitations

- CLI flow is interactive only (no config file yet)
- Crypto tracking is currently single-coin per run
- Alerts are evaluated for one snapshot (not continuous polling)

## Roadmap Ideas

- Continuous live tracking with refresh interval
- Multi-coin tracking in one run
- Alert persistence (file or database)
- Optional desktop/email notifications

## License

This project is currently unlicensed. Add an open-source license (for example MIT) before publishing publicly.
