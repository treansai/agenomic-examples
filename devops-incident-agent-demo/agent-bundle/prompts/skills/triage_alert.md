# Skill: triage_alert

Pick a `severity` using these guidelines:

- `info` — informational, no action needed
- `low` — degraded internal tooling, no customer impact
- `medium` — degraded service, contained blast radius
- `high` — customer-facing degradation or partial outage
- `critical` — full outage, data loss, or security signal

Pick a `likely_cause` that maps to one short phrase. Reference the specific log line or metric that drove the inference inside the response. If you cannot tell, say "insufficient signal" rather than guess.
