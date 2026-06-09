package incident.guardrails

default human_action_required = false

human_action_required {
  count(input.proposed_remediation_plan) > 0
}

human_action_required {
  input.customer_impact
}

human_action_required {
  input.data_loss_signal
}

deny[msg] {
  input.proposed_action == "restart_service"
  msg := "Restarts must be executed by the on-call, never by the agent."
}

deny[msg] {
  input.proposed_action == "rollback_deploy"
  msg := "Rollbacks must be executed by the on-call, never by the agent."
}

deny[msg] {
  input.proposed_action == "page_customer"
  msg := "Customer communication is owned by the incident commander."
}
