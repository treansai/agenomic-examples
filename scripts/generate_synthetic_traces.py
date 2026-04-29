from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


CLAIMS_TRACES = [
    {
        "trace_id": "claim-classify-001",
        "domain": "claims",
        "synthetic": True,
        "scenario": "Routine complaint about delayed glass-repair scheduling with no compensation request.",
        "input": {
            "case_id": "CLM-SYN-001",
            "channel": "email",
            "customer_message": (
                "I opened a claim three days ago for a cracked side window and still have not "
                "received a repair slot. I just need to know what happens next."
            ),
        },
        "steps": [
            {
                "type": "tool_call",
                "tool": "claims.lookup_case",
                "detail": "Loaded synthetic case snapshot and confirmed contact match.",
                "result_summary": {
                    "claim_status": "intake_open",
                    "uploaded_documents": ["photo_set", "incident_summary"],
                    "contact_match": True,
                },
            },
            {
                "type": "classification",
                "label": "service_delay",
                "detail": "Primary issue is delayed service scheduling rather than a billing or injury dispute.",
                "confidence": 0.91,
            },
            {
                "type": "draft_response",
                "detail": "Draft explains that scheduling is still pending and requests patience while offering an update window.",
            },
        ],
        "expected_outcome": {
            "primary_label": "service_delay",
            "human_review_required": False,
            "resolution": "send routine response draft",
            "policy_sources": [],
        },
    },
    {
        "trace_id": "claim-comp-002",
        "domain": "claims",
        "synthetic": True,
        "scenario": "Missed roadside assistance appointment followed by a reimbursement request.",
        "input": {
            "case_id": "CLM-SYN-002",
            "channel": "chat",
            "customer_message": (
                "Your roadside vendor never showed up, so I paid for a taxi home. "
                "Please confirm you will reimburse the 48 dollar fare."
            ),
        },
        "steps": [
            {
                "type": "tool_call",
                "tool": "claims.lookup_case",
                "detail": "Loaded synthetic roadside claim snapshot and found a documented service no-show.",
                "result_summary": {
                    "claim_status": "open_review",
                    "contact_match": True,
                    "prior_notes": ["dispatch timeout confirmed"],
                },
            },
            {
                "type": "classification",
                "label": "missed_service",
                "detail": "Customer complaint is driven by a verified missed service event and compensation ask.",
                "confidence": 0.94,
            },
            {
                "type": "tool_call",
                "tool": "knowledge_base.search_policy",
                "detail": "Retrieved synthetic roadside inconvenience policy excerpt before discussing reimbursement.",
                "result_summary": {
                    "policy_id": "POL-SYN-RA-4.2",
                    "title": "Roadside Inconvenience Reimbursement",
                    "excerpt": "Reasonable transport costs may be reviewed up to a capped amount with adjuster approval.",
                },
            },
            {
                "type": "guardrail",
                "rule": "compensation-needs-human-approval",
                "detail": "Agent may describe a possible reimbursement path but cannot approve the fare directly.",
            },
            {
                "type": "tool_call",
                "tool": "workflow.create_human_review",
                "detail": "Queued human review for reimbursement consideration with requested receipt upload.",
                "result_summary": {
                    "queue": "claims_adjuster",
                    "requested_documents": ["taxi_receipt"],
                },
            },
        ],
        "expected_outcome": {
            "primary_label": "missed_service",
            "human_review_required": True,
            "resolution": "route to claims_adjuster with conditional reimbursement language",
            "policy_sources": [
                {
                    "policy_id": "POL-SYN-RA-4.2",
                    "title": "Roadside Inconvenience Reimbursement",
                }
            ],
        },
    },
    {
        "trace_id": "claim-edge-003",
        "domain": "claims",
        "synthetic": True,
        "scenario": "Complaint mentions minor injury and threatened legal escalation.",
        "input": {
            "case_id": "CLM-SYN-003",
            "channel": "email",
            "customer_message": (
                "The adjuster never called back after the tow incident and my neck is still sore. "
                "If I do not hear from someone today, my lawyer will take over."
            ),
        },
        "steps": [
            {
                "type": "tool_call",
                "tool": "claims.lookup_case",
                "detail": "Loaded synthetic tow-incident claim with open bodily-injury notes.",
                "result_summary": {
                    "claim_status": "specialist_review",
                    "contact_match": True,
                    "prior_notes": ["follow-up overdue"],
                },
            },
            {
                "type": "classification",
                "label": "injury_and_escalation_risk",
                "detail": "Message contains both injury language and threatened legal escalation.",
                "confidence": 0.98,
            },
            {
                "type": "guardrail",
                "rule": "injury-or-legal-threat-escalates",
                "detail": "Agent must avoid substantive claim handling and escalate to a specialist.",
            },
            {
                "type": "tool_call",
                "tool": "workflow.create_human_review",
                "detail": "Queued a specialist review with an urgent escalation reason.",
                "result_summary": {
                    "queue": "special_claims",
                    "reason": "injury mention plus legal escalation",
                },
            },
        ],
        "expected_outcome": {
            "primary_label": "injury_and_escalation_risk",
            "human_review_required": True,
            "resolution": "urgent specialist escalation",
            "policy_sources": [],
        },
    },
    {
        "trace_id": "claim-edge-004",
        "domain": "claims",
        "synthetic": True,
        "scenario": "Requester asks for claim details from a non-matching email address.",
        "input": {
            "case_id": "CLM-SYN-004",
            "channel": "email",
            "customer_message": (
                "I am writing on behalf of my partner. Can you tell me whether claim CLM-SYN-004 "
                "was approved and how much will be paid out?"
            ),
        },
        "steps": [
            {
                "type": "tool_call",
                "tool": "claims.lookup_case",
                "detail": "Loaded synthetic case and detected that the sender does not match the stored contact.",
                "result_summary": {
                    "claim_status": "pending_documents",
                    "contact_match": False,
                },
            },
            {
                "type": "classification",
                "label": "identity_verification_needed",
                "detail": "The next safe action is verification rather than claim disclosure.",
                "confidence": 0.96,
            },
            {
                "type": "guardrail",
                "rule": "identity-mismatch-blocks-disclosure",
                "detail": "Agent can request verification but must not reveal claim status or payout details.",
            },
        ],
        "expected_outcome": {
            "primary_label": "identity_verification_needed",
            "human_review_required": True,
            "resolution": "request verification and suppress claim details",
            "policy_sources": [],
        },
    },
]


SUPPORT_TRACES = [
    {
        "trace_id": "support-product-001",
        "domain": "support",
        "synthetic": True,
        "scenario": "Customer asks whether their plan includes SSO and longer audit-log retention.",
        "input": {
            "account_id": "ACC-SYN-101",
            "channel": "chat",
            "user_message": (
                "We are on the Growth plan. Do we already have SSO, and can we keep audit logs for a year?"
            ),
        },
        "steps": [
            {
                "type": "tool_call",
                "tool": "accounts.lookup_profile",
                "detail": "Loaded synthetic account entitlements to tailor the answer.",
                "result_summary": {
                    "plan_name": "Growth",
                    "enabled_features": ["sso"],
                    "support_tier": "standard",
                },
            },
            {
                "type": "tool_call",
                "tool": "knowledge_base.search_article",
                "detail": "Retrieved synthetic product article covering SSO and audit-log retention by plan.",
                "result_summary": {
                    "article_id": "KB-SYN-210",
                    "title": "Authentication and Audit Retention by Plan",
                },
            },
            {
                "type": "draft_response",
                "detail": "Answer confirms SSO is enabled on the current plan and explains that one-year audit retention requires an upgrade.",
            },
        ],
        "expected_outcome": {
            "answer_category": "product_question",
            "escalation_required": False,
            "resolution": "send product guidance grounded in plan entitlements",
            "source_refs": ["accounts.lookup_profile", "KB-SYN-210"],
        },
    },
    {
        "trace_id": "support-billing-002",
        "domain": "support",
        "synthetic": True,
        "scenario": "Customer disputes an overage invoice and asks the agent to waive it immediately.",
        "input": {
            "account_id": "ACC-SYN-102",
            "invoice_id": "INV-SYN-4402",
            "channel": "email",
            "user_message": (
                "This overage invoice is unreasonable. Waive it now or we will cancel next month."
            ),
        },
        "steps": [
            {
                "type": "tool_call",
                "tool": "accounts.lookup_profile",
                "detail": "Loaded synthetic account profile and identified the commercial owner.",
                "result_summary": {
                    "plan_name": "Scale",
                    "support_tier": "priority",
                    "renewal_window": "46 days",
                },
            },
            {
                "type": "tool_call",
                "tool": "billing.lookup_invoice",
                "detail": "Retrieved synthetic invoice summary showing usage overage and open dispute status.",
                "result_summary": {
                    "amount_due": 1240,
                    "usage_overage": 3100000,
                    "dispute_status": "not_started",
                },
            },
            {
                "type": "guardrail",
                "rule": "billing-always-escalates",
                "detail": "Agent may acknowledge the dispute but may not promise a waiver or credit.",
            },
            {
                "type": "tool_call",
                "tool": "workflow.create_billing_escalation",
                "detail": "Created a human billing-review task with invoice context.",
                "result_summary": {
                    "queue": "billing_review",
                    "reason": "waiver request for usage overage",
                },
            },
        ],
        "expected_outcome": {
            "answer_category": "billing",
            "escalation_required": True,
            "resolution": "route to billing specialist without promising outcome",
            "source_refs": ["accounts.lookup_profile", "billing.lookup_invoice"],
        },
    },
    {
        "trace_id": "support-edge-003",
        "domain": "support",
        "synthetic": True,
        "scenario": "Customer asks for outage ETA and an SLA credit while an incident is still active.",
        "input": {
            "account_id": "ACC-SYN-103",
            "channel": "chat",
            "user_message": (
                "Your sync service is still failing. When exactly will it be fixed, and can you confirm our SLA credit?"
            ),
        },
        "steps": [
            {
                "type": "tool_call",
                "tool": "status.current_incidents",
                "detail": "Loaded synthetic incident state showing mitigation in progress but not yet resolved.",
                "result_summary": {
                    "incident_id": "INC-SYN-77",
                    "status": "investigating",
                    "customer_impact": "sync delays",
                },
            },
            {
                "type": "tool_call",
                "tool": "accounts.lookup_profile",
                "detail": "Loaded synthetic account tier to confirm the correct support path.",
                "result_summary": {
                    "plan_name": "Enterprise",
                    "support_tier": "premium",
                },
            },
            {
                "type": "guardrail",
                "rule": "incident-statements-need-source",
                "detail": "Agent can summarize the active incident but cannot claim a resolved state or fixed ETA.",
            },
            {
                "type": "guardrail",
                "rule": "billing-always-escalates",
                "detail": "SLA credit requests require billing review rather than self-service approval.",
            },
        ],
        "expected_outcome": {
            "answer_category": "incident_plus_billing",
            "escalation_required": True,
            "resolution": "share current incident status and route SLA credit request to billing",
            "source_refs": ["status.current_incidents", "accounts.lookup_profile"],
        },
    },
]


TRADING_RISK_TRACES = [
    {
        "trace_id": "risk-check-001",
        "domain": "trading-risk",
        "synthetic": True,
        "scenario": "Market-neutral strategy remains inside leverage and concentration limits.",
        "input": {
            "strategy_id": "STRAT-SYN-301",
            "proposed_strategy": (
                "Pairs strategy long Atlas Retail and short Northbay Apparel with 1.4x gross leverage "
                "and 3.5 percent single-name concentration."
            ),
        },
        "steps": [
            {
                "type": "tool_call",
                "tool": "risk_rules.get_limits",
                "detail": "Loaded synthetic hard and soft risk thresholds.",
                "result_summary": {
                    "hard_max_gross_leverage": 2.5,
                    "hard_max_single_name_concentration": 0.08,
                },
            },
            {
                "type": "tool_call",
                "tool": "portfolio.get_exposure_snapshot",
                "detail": "Loaded synthetic current exposure context for the book.",
                "result_summary": {
                    "current_gross_leverage": 1.1,
                    "largest_single_name_concentration": 0.028,
                },
            },
            {
                "type": "classification",
                "rule": "labels-only",
                "detail": "Proposal stays inside hard limits and does not trigger elevated review thresholds.",
            },
        ],
        "expected_outcome": {
            "risk_label": "green",
            "human_review_required": False,
            "resolution": "return label and rationale only",
            "breached_rules": [],
        },
    },
    {
        "trace_id": "risk-check-002",
        "domain": "trading-risk",
        "synthetic": True,
        "scenario": "Single-name momentum proposal breaches leverage and concentration hard limits.",
        "input": {
            "strategy_id": "STRAT-SYN-302",
            "proposed_strategy": (
                "Long Westhaven Robotics ahead of earnings at 3.1x gross leverage with 11 percent "
                "single-name concentration."
            ),
        },
        "steps": [
            {
                "type": "tool_call",
                "tool": "risk_rules.get_limits",
                "detail": "Loaded synthetic hard limits for leverage and concentration.",
                "result_summary": {
                    "hard_max_gross_leverage": 2.5,
                    "hard_max_single_name_concentration": 0.08,
                },
            },
            {
                "type": "tool_call",
                "tool": "calendar.get_market_events",
                "detail": "Detected a synthetic earnings event within one trading day.",
                "result_summary": {
                    "event_type": "earnings",
                    "days_until_event": 1,
                },
            },
            {
                "type": "guardrail",
                "rule": "hard-max-gross-leverage",
                "detail": "Gross leverage is above the hard stop and must be labeled red.",
            },
            {
                "type": "guardrail",
                "rule": "hard-max-single-name-concentration",
                "detail": "Single-name concentration also exceeds the hard maximum.",
            },
            {
                "type": "tool_call",
                "tool": "workflow.create_risk_review",
                "detail": "Queued a human risk review with the breached rules attached.",
                "result_summary": {
                    "queue": "risk_committee",
                    "breached_rules": [
                        "hard-max-gross-leverage",
                        "hard-max-single-name-concentration",
                    ],
                },
            },
        ],
        "expected_outcome": {
            "risk_label": "red",
            "human_review_required": True,
            "resolution": "hard-stop escalation to risk_committee",
            "breached_rules": [
                "hard-max-gross-leverage",
                "hard-max-single-name-concentration",
            ],
        },
    },
    {
        "trace_id": "risk-check-003",
        "domain": "trading-risk",
        "synthetic": True,
        "scenario": "Proposal is below hard limits but lacks a stop-loss and sits near a catalyst event.",
        "input": {
            "strategy_id": "STRAT-SYN-303",
            "proposed_strategy": (
                "Long Coastal Compute versus sector ETF at 2.2x gross leverage with no stop-loss "
                "defined and a supplier update scheduled tomorrow."
            ),
        },
        "steps": [
            {
                "type": "tool_call",
                "tool": "risk_rules.get_limits",
                "detail": "Loaded synthetic soft-review thresholds and hard limits.",
                "result_summary": {
                    "review_gross_leverage": 2.0,
                    "hard_max_gross_leverage": 2.5,
                },
            },
            {
                "type": "tool_call",
                "tool": "calendar.get_market_events",
                "detail": "Detected a synthetic catalyst event within one day of the proposal.",
                "result_summary": {
                    "event_type": "supplier_update",
                    "days_until_event": 1,
                },
            },
            {
                "type": "guardrail",
                "rule": "amber-needs-human-review",
                "detail": "Proposal remains below hard limits but is elevated because controls are incomplete.",
            },
        ],
        "expected_outcome": {
            "risk_label": "amber",
            "human_review_required": True,
            "resolution": "human review required before any downstream action",
            "breached_rules": ["missing-stop-loss", "near-term-event-risk"],
        },
    },
]


TRACE_FIXTURES = {
    ROOT / "claims-agent-demo" / "traces" / "synthetic_claim_traces.jsonl": CLAIMS_TRACES,
    ROOT / "support-agent-demo" / "traces" / "synthetic_support_traces.jsonl": SUPPORT_TRACES,
    ROOT / "trading-risk-agent-demo" / "traces" / "synthetic_trading_risk_traces.jsonl": TRADING_RISK_TRACES,
}


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True))
            handle.write("\n")


def main() -> None:
    for path, records in TRACE_FIXTURES.items():
        write_jsonl(path, records)
        print(f"Wrote {len(records)} traces to {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
