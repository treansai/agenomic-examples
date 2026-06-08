# Skill: produce_signal

Pick `signal` from {long, short, flat}. Bias toward `flat` when:

- price action is inside the recent range with no breakout
- news_volatility is `extreme`
- the next earnings print is within 2 trading days
- confidence calibrates below 0.55

Confidence is an estimate, not a probability of profit. Calibrate by:

- 0.85+ : multiple independent signals aligned, low headline risk
- 0.65 - 0.85 : one strong signal, no conflicting evidence
- 0.55 - 0.65 : weak edge, easy to invalidate
- below 0.55 : do not call directional — return `flat`
