# Skill: classify_line_item

For each line item, infer the `category` from the vendor name and the description, never from amount alone. If the vendor or description suggests a personal expense (alcohol-heavy bar, weekend leisure, family member named), set `category="personal_suspected"` and `personal_expense_suspected=true` at the report level. Do not recategorize personal as business.
