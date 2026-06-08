# Skill: recommend_controls

Map the label to a baseline set of controls:

- `public` — none required
- `internal` — restrict to authenticated employees; no external sharing without approval
- `confidential` — encryption at rest; access via least-privilege role; audit log on read
- `restricted` — encryption at rest + in transit; per-record access approval; DPO review on export; KMS-managed keys

When credentials are detected, add: "rotate the credential and revoke any cached token". When `government_id` or `health_record` is detected, add: "isolate in the regulated-data zone and notify the DPO".
