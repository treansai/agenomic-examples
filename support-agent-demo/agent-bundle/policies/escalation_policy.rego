package support.escalation

requires_human_review {
  input.issue_category == "billing"
}

requires_human_review {
  input.user_requests_credit
}

deny[msg] {
  input.proposed_action == "grant_credit"
  msg := "Credits and refunds must be handled by a human billing specialist."
}

deny[msg] {
  input.promise_type == "roadmap_date"
  msg := "Feature delivery dates cannot be promised without an approved source."
}

deny[msg] {
  input.incident_statement == "resolved"
  input.incident_status != "resolved"
  msg := "Incident status must match the approved source."
}
