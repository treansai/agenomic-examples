# Skill: propose_remediation

The `proposed_remediation_plan` must be:

- a short array of imperative steps (5 steps max)
- phrased for a human on-call to execute
- ordered: safer reversible steps before destructive steps
- explicit about pre-flight checks (e.g., "confirm replica lag before failover")

Never include a step that the agent will perform itself. Never include customer communication steps — those are owned by the incident commander, not this agent.
