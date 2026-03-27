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

## Example Output

```text
=== Currency and Crypto Tracker ===
Enter base currency code (example: USD): USD
Enter target currency codes separated by commas (example: TRY,EUR): TRY,EUR
Enter crypto coin id to track (example: bitcoin): bitcoin
Enter quote currency for crypto price (example: usd): usd

--- Live Snapshot ---
USD/TRY: 38.9120
USD/EUR: 0.9210
BITCOIN/USD: 68215.31

--- Alert Rules (Optional) ---
Would you like to add a forex alert? (y/n): y
Alert direction ('above' or 'below'): above
Enter threshold value: 38.0
Would you like to add a crypto alert? (y/n): n

--- Alert Results ---
[ALERT] USD/TRY is 38.9120 and moved above 38.0000.
```

## Known Limitations

- CLI flow is interactive only (no config file or command-line flags yet)
- Crypto tracking supports a single coin per run
- Alerts are evaluated only once per execution (no continuous polling loop)
- No persistent storage layer (alert history is not saved to disk/database)

## Roadmap Ideas

- Continuous live tracking with refresh interval
- Multi-coin tracking in one run
- Alert persistence (file or database)
- Optional desktop/email notifications

## Suggested GitHub Topics

If you want your repository to be easier to discover, add these topics in GitHub:

- `python`
- `cli`
- `api-client`
- `forex`
- `cryptocurrency`
- `market-tracker`

## Release Checklist (v1.0.0)

- [x] Core application modules implemented
- [x] Unit tests added and passing
- [x] GitHub Actions CI added
- [x] Documentation and setup instructions completed
- [ ] Create a GitHub Release named `v1.0.0`

## License

MIT License
