package dlp.guardrails

default human_review_required = false

human_review_required {
  input.sensitivity_label == "restricted"
}

human_review_required {
  input.credentials_detected
}

human_review_required {
  input.government_id_detected
}

human_review_required {
  input.health_record_detected
}

deny[msg] {
  input.proposed_action == "echo_full_pii"
  msg := "Full PII values must not be echoed back to the caller."
}

deny[msg] {
  input.proposed_action == "apply_dlp_action"
  msg := "DLP actions must be approved by the DPO, not the agent."
}
