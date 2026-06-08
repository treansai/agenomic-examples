# Skill: check_margin

Given the proposed order, account snapshot, and market snapshot:

- `notional = abs(size) * mark_price`
- `leverage_ratio = notional / account_equity`
- `notional_pct_of_equity = 100 * notional / account_equity`
- For a perp with maintenance margin `mm` (default 0.05 if not given): approximate `liquidation_distance_pct` from current mark using

  - long:  `(entry - liq) / entry * 100` with `liq ≈ entry * (1 - 1/leverage + mm)`
  - short: `(liq - entry) / entry * 100` with `liq ≈ entry * (1 + 1/leverage - mm)`

Round to one decimal. Use the `market_snapshot.mark_price` as entry if no other entry is provided.
