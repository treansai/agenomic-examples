package trading.risk

deny[msg] {
  input.proposed_action == "place_trade"
  msg := "This agent may not place trades."
}

deny[msg] {
  input.proposed_action == "create_order_ticket"
  msg := "This agent may not generate executable order tickets."
}

red[msg] {
  input.gross_leverage > 2.5
  msg := "Gross leverage exceeds the hard limit."
}

red[msg] {
  input.single_name_concentration > 0.08
  msg := "Single-name concentration exceeds the hard limit."
}

requires_human_review {
  input.gross_leverage > 2.0
}

requires_human_review {
  not input.stop_loss_defined
}
