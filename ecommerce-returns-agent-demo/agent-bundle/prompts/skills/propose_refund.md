# Skill: propose_refund

Refund computation:

- default = full item price + shipping, if the reason is `defective`, `wrong_item`, `damaged_in_transit`, `not_as_described`, or `late_delivery`
- default = item price minus restocking fee per policy, for `changed_mind`
- never propose more than `autonomous_refund_cap_eur` without setting `amount_above_cap=true` and `human_review_required=true`
- always echo the cap and the proposed amount in the `response_draft` so the customer sees the math
