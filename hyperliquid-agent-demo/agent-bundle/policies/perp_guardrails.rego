package perp.guardrails

default human_confirmation_required = true

max_leverage := 10
min_liquidation_distance_pct := 8
max_notional_pct := 25

deny[msg] {
  input.proposed_action == "sign_transaction"
  msg := "Signing transactions is owned by the user wallet, not this agent."
}

deny[msg] {
  input.proposed_action == "withdraw_funds"
  msg := "The agent cannot move user funds."
}

reduce_required {
  input.leverage_ratio > max_leverage
}

reduce_required {
  input.liquidation_distance_pct < min_liquidation_distance_pct
}

reduce_required {
  input.notional_pct_of_equity > max_notional_pct
}

reject_required {
  input.leverage_ratio > 25
}

reject_required {
  input.liquidation_distance_pct < 3
}
