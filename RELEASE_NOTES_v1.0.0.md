# v1.0.0 Release Notes

## Summary

First stable release of the Currency and Crypto Tracker CLI project.

## Included

- Modular architecture with separate API, tracking, and application entry modules
- Live forex rates via Frankfurter API
- Live crypto prices via CoinGecko API
- Threshold-based alert evaluation (`above` / `below`)
- Input validation and user-friendly error handling
- Unit tests for API parsing and alert logic
- GitHub Actions CI workflow for automated test runs
- Complete setup and usage documentation in `README.md`

## Known Limitations

- Interactive CLI only
- Single-coin tracking per run
- Snapshot-based alerts (no continuous polling)
- No persistent alert history

## Next Iteration Candidates

- Scheduled polling mode
- Multi-coin tracking
- Config file support
- Alert logging and notification channels
