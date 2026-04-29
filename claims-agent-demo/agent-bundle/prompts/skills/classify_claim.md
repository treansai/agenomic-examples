# Skill: classify_claim

Classify the complaint using the smallest label that explains the main issue.

Preferred labels:

- `service_delay`
- `missed_service`
- `documentation_gap`
- `billing_dispute`
- `injury_and_escalation_risk`
- `identity_verification_needed`

Guidance:

- Use `injury_and_escalation_risk` when the message mentions injury, lawyers, regulators, or public escalation.
- Use `identity_verification_needed` when the requester cannot be matched to the claim contact.
- If several issues are present, pick the label that most directly drives the next action.
- Return a confidence score and the signals that caused the classification.
