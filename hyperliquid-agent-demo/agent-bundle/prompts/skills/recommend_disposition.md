# Skill: recommend_disposition

Disposition logic, applied in order:

1. `reject` — order is structurally impossible (size <= 0, missing side, asset not in the venue's universe)
2. `reject` — `leverage_ratio > 25` or `liquidation_distance_pct < 3` (clearly hostile risk)
3. `reduce_size` — any single limit breached but the trade has an obviously safer size:
   - `leverage_ratio > 10`
   - `liquidation_distance_pct < 8`
   - `notional_pct_of_equity > 25`
   Suggest a `suggested_size_adjustment` that brings the most binding limit back inside policy.
4. `accept_for_human_confirmation` — every limit respected

Even on acceptance, the human must click. Reflect that in `human_confirmation_required=true`.
