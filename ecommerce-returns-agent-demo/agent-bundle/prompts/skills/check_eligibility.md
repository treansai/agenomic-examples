# Skill: check_eligibility

Eligibility comes from three signals, in order:

1. is the order within `return_window_days` of delivery?
2. is the SKU category in the excluded set?
3. is there a fraud signal on the order snapshot?

If any of (1), (2), (3) fail, set `eligibility_status="needs_review"` and the matching boolean flag. Never mark an order `ineligible` on a borderline case — defer to a human.
