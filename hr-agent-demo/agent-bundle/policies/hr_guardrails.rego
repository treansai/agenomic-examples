package hr.guardrails

default human_review_required = false

human_review_required {
  input.leave_approval_requested
}

human_review_required {
  input.policy_exception_requested
}

human_review_required {
  input.other_employee_data_requested
}

deny[msg] {
  input.proposed_action == "approve_leave"
  msg := "Leave approvals must go through the employee's manager."
}

deny[msg] {
  input.proposed_action == "modify_payroll"
  msg := "Payroll changes cannot be performed by the agent."
}

deny[msg] {
  input.proposed_action == "disclose_other_employee_record"
  msg := "Other-employee records cannot be disclosed."
}
