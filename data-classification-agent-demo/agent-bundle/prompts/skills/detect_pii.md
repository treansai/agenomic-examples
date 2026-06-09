# Skill: detect_pii

Look for these patterns. List every category found in `detected_categories`. Do not echo the value itself.

- `email_address` — `name@domain.tld`
- `phone_number` — international or local form
- `credit_card_pan` — 13-19 digit sequence, optionally Luhn-valid
- `iban` — country code + check digits + BBAN
- `government_id` — passport, SSN, national ID style
- `health_record` — diagnosis, ICD code, treatment note
- `credentials` — passwords, API tokens, JWTs, private keys, OAuth secrets
- `location_precise` — full street address or lat/lon to >4 decimals

For each detection, you may push one masked fragment into `evidence_masked` (e.g., `"card: **** **** **** 4242"`, `"email: a***@e***.com"`). Never the full value.
