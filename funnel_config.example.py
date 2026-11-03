"""
Business Onboarding Funnel Config — Example
============================================
Copy this file to funnel_config.py and fill in your calibrated values.
funnel_config.py is gitignored — this example shows the structure only.

Conversion rates and time distributions were derived from real business
onboarding data. Fix recommendations are based on root-cause analysis
of where and why businesses dropped off at each step.
"""

# ── Stage conversion rates (probability of completing each step) ──────────────
# Calibrated from real onboarding data — not included in this demo repo.
STAGE_CONVERSION_RATES = {
    "business_profile":  None,   # % who complete profile after signup
    "campaign_brief":    None,   # % who write a brief after profile — typically the worst drop
    "creator_selection": None,   # % who select a creator after writing brief
    "campaign_live":     None,   # % who go live after selecting creator
}

# ── Average time per step (mean_minutes, std_minutes) ────────────────────────
# Calibrated from session timing data — not included in this demo repo.
COMPLETER_TIME = {
    "signup":            (None, None),
    "business_profile":  (None, None),
    "campaign_brief":    (None, None),   # longest step — confusion point
    "creator_selection": (None, None),
    "campaign_live":     (None, None),
}

# ── Fix recommendations per step ─────────────────────────────────────────────
# Based on root-cause analysis of dropout patterns — proprietary PM analysis.
FIX_RECOMMENDATIONS = {
    "signup":            None,
    "business_profile":  None,
    "campaign_brief":    None,
    "creator_selection": None,
    "campaign_live":     None,
}
