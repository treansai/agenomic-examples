package expense.guardrails

default human_review_required = false

meal_per_diem := 60
hotel_cap := 250
receipt_threshold := 25

human_review_required {
  input.has_policy_violation
}

human_review_required {
  input.has_missing_receipt
}

human_review_required {
  input.personal_expense_suspected
}

deny[msg] {
  input.proposed_action == "approve_expense"
  msg := "Approvals are reserved for the finance reviewer."
}

deny[msg] {
  input.proposed_action == "recategorize"
  input.original_category == "personal_suspected"
  msg := "Personal expenses cannot be re-categorized as business."
}
