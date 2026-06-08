package returns.guardrails

default human_review_required = false

autonomous_cap_eur := 80
return_window_days := 30

human_review_required {
  input.proposed_refund_amount > autonomous_cap_eur
}

human_review_required {
  input.days_since_delivery > return_window_days
}

human_review_required {
  input.category == "perishables"
}

human_review_required {
  input.category == "custom"
}

human_review_required {
  input.category == "hygiene"
}

human_review_required {
  input.fraud_signal
}

deny[msg] {
  input.proposed_action == "issue_refund"
  input.proposed_refund_amount > autonomous_cap_eur
  msg := "Refunds above the autonomous cap require a human reviewer."
}
