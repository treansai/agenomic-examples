# Skill: recommend_disposition

- `approve_within_policy` — every line is compliant, no missing receipts, no over-cap items
- `clarify` — only missing receipts on otherwise-compliant lines
- `escalate` — any policy violation, over-cap line, or personal expense suspected

Whenever you escalate, also set `human_review_required=true` with a concise `human_review_reason` referencing the offending line indexes.
