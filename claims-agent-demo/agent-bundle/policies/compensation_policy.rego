package claims.compensation

default human_review_required = false

human_review_required {
  input.compensation_requested
}

deny[msg] {
  input.proposed_action == "commit_compensation"
  msg := "Compensation commitments require human approval."
}

deny[msg] {
  input.proposed_action == "suggest_compensation"
  count(input.policy_sources) == 0
  msg := "Compensation suggestions must cite at least one policy source."
}

deny[msg] {
  not input.identity_verified
  input.proposed_action == "disclose_claim_details"
  msg := "Claim details cannot be disclosed before identity verification."
}
