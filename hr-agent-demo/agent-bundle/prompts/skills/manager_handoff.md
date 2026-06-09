# Skill: manager_handoff

When the employee asks for an approval, an exception, or a payroll change:

- set `human_review_required=true`
- set the matching trigger flag (`leave_approval_requested`, `policy_exception_requested`, ...)
- write a `human_review_reason` that names the manager or HR partner that should pick this up
- the `response_draft` must acknowledge the request and explain that a human will follow up — it must not pre-approve or pre-deny
