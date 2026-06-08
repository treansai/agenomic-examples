package signals.guardrails

default human_review_required = false

human_review_required {
  input.confidence < 0.55
}

human_review_required {
  input.earnings_window
}

human_review_required {
  input.news_volatility == "extreme"
}

deny[msg] {
  input.proposed_action == "place_order"
  msg := "Order placement is owned by the execution system, not the signal agent."
}

deny[msg] {
  input.signal != "long"
  input.signal != "short"
  input.signal != "flat"
  msg := "Signal must be one of long, short, flat."
}
