"""
Froker Business Onboarding Drop-off Analyzer
=============================================
Identifies the exact onboarding step where local businesses abandon
the flow, compares completers vs droppers, and outputs one fix per step.

Built Aug 2024 – Aug 2025 — pure Python + SQLite demo.

Problem:
  Local businesses sign up but most never post their first campaign.
  They are small business owners, not marketers — the onboarding
  confuses them. No one had measured exactly where they quit.

Onboarding steps:
  1. Business signup (name, category, location)
  2. Business profile (description, logo, opening hours)
  3. Campaign brief (what do you want creators to post?)
  4. Creator selection (pick from recommended creators)
  5. First campaign live (deal confirmed with a creator)
"""

import random
import sqlite3
from datetime import datetime, timedelta

random.seed(99)

# ── Demo dataset ─────────────────────────────────────────────────────────────

STEPS = [
    "signup",
    "business_profile",
    "campaign_brief",
    "creator_selection",
    "campaign_live",
]

STEP_LABELS = {
    "signup":            "Step 1 — Signup",
    "business_profile":  "Step 2 — Business Profile",
    "campaign_brief":    "Step 3 — Campaign Brief",
    "creator_selection": "Step 4 — Creator Selection",
    "campaign_live":     "Step 5 — Campaign Live",
}

# Time-to-complete per step (minutes) — completers
COMPLETER_TIME = {
    "signup":            (3, 1),
    "business_profile":  (8, 3),
    "campaign_brief":    (18, 7),  # this step takes long — confusion point
    "creator_selection": (6, 2),
    "campaign_live":     (2, 1),
}

def make_businesses():
    base = datetime(2024, 9, 1)
    businesses = []
    n = 150

    for i in range(n):
        signup_ts = base + timedelta(days=random.randint(0, 60),
                                      hours=random.randint(9, 21))
        row = {
            "biz_id":   f"DEMO_BIZ_{i+1:03d}",
            "signup_ts": signup_ts,
        }
        prev_ts = signup_ts

        # Step 1: everyone completes signup
        row["signup_done_ts"] = prev_ts + timedelta(minutes=max(1, random.gauss(*COMPLETER_TIME["signup"])))
        prev_ts = row["signup_done_ts"]

        # Step 2: 82% complete profile
        if random.random() < 0.82:
            row["profile_done_ts"] = prev_ts + timedelta(minutes=max(1, random.gauss(*COMPLETER_TIME["business_profile"])))
            prev_ts = row["profile_done_ts"]
        else:
            businesses.append(row); continue

        # Step 3: only 44% write a brief (WORST DROP — confusing form)
        if random.random() < 0.44:
            row["brief_done_ts"] = prev_ts + timedelta(minutes=max(5, random.gauss(*COMPLETER_TIME["campaign_brief"])))
            prev_ts = row["brief_done_ts"]
        else:
            businesses.append(row); continue

        # Step 4: 78% select a creator
        if random.random() < 0.78:
            row["creator_selected_ts"] = prev_ts + timedelta(minutes=max(1, random.gauss(*COMPLETER_TIME["creator_selection"])))
            prev_ts = row["creator_selected_ts"]
        else:
            businesses.append(row); continue

        # Step 5: 91% go live
        if random.random() < 0.91:
            row["campaign_live_ts"] = prev_ts + timedelta(minutes=max(1, random.gauss(*COMPLETER_TIME["campaign_live"])))

        businesses.append(row)

    return businesses

DEMO_BUSINESSES = make_businesses()


# ── Analysis ──────────────────────────────────────────────────────────────────

STEP_COLUMNS = {
    "signup":            ("signup_done_ts",      None),
    "business_profile":  ("profile_done_ts",     "signup_done_ts"),
    "campaign_brief":    ("brief_done_ts",        "profile_done_ts"),
    "creator_selection": ("creator_selected_ts",  "brief_done_ts"),
    "campaign_live":     ("campaign_live_ts",     "creator_selected_ts"),
}

FIX_RECOMMENDATIONS = {
    "signup":            "Reduce signup fields to 3 essentials (name, category, phone). Defer logo/hours.",
    "business_profile":  "Add autofill from Google Maps — business description pre-populates from their GMB listing.",
    "campaign_brief":    "Replace open-form brief with a 5-question wizard + example prompts per category. This is the #1 confusion point.",
    "creator_selection": "Show only 3 pre-matched creators, not a full grid. Too much choice causes abandonment.",
    "campaign_live":     "Add a 'confirm in 1 tap' option. Current 3-step confirmation is overkill.",
}


def run_analysis() -> None:
    print("\n" + "="*65)
    print("  FROKER BUSINESS ONBOARDING FUNNEL ANALYSIS")
    print("="*65 + "\n")

    total = len(DEMO_BUSINESSES)

    def count_reached(col: str) -> int:
        return sum(1 for b in DEMO_BUSINESSES if b.get(col) is not None)

    def avg_time_minutes(done_col: str, start_col: str | None) -> float:
        times = []
        for b in DEMO_BUSINESSES:
            if b.get(done_col) and (start_col is None or b.get(start_col)):
                start = b[start_col] if start_col else b["signup_ts"]
                delta = (b[done_col] - start).total_seconds() / 60
                if 0 < delta < 120:
                    times.append(delta)
        return sum(times) / len(times) if times else 0.0

    prev_n = total
    worst_drop_pct = 0.0
    worst_step = ""

    rows = []
    for step in STEPS:
        done_col, start_col = STEP_COLUMNS[step]
        n        = count_reached(done_col)
        drop_pct = (1 - n / prev_n) * 100 if prev_n > 0 else 0
        avg_min  = avg_time_minutes(done_col, start_col)
        rows.append((step, n, drop_pct, avg_min))
        if drop_pct > worst_drop_pct and step != "signup":
            worst_drop_pct = drop_pct
            worst_step = step
        prev_n = n

    print(f"  {'Step':<30} {'Reached':>8} {'Conv%':>7} {'Drop%':>7} {'Avg min':>9}")
    print("  " + "-"*60)
    prev_n = total
    for step, n, drop_pct, avg_min in rows:
        conv_pct = n / total * 100
        flag = " ← WORST DROP" if step == worst_step else ""
        print(f"  {STEP_LABELS[step]:<30} {n:>8} {conv_pct:>6.1f}% {drop_pct:>6.1f}% {avg_min:>8.1f}m{flag}")
        prev_n = n

    print(f"\n\n  KEY FINDING:")
    print(f"  ⚠️  {STEP_LABELS[worst_step]} — {worst_drop_pct:.1f}% drop")
    print(f"\n  TIME SIGNAL:")
    brief_row = next(r for r in rows if r[0] == "campaign_brief")
    print(f"  Businesses that reach the brief step spend {brief_row[3]:.0f} min avg on it.")
    print(f"  Businesses that complete it convert at 78% to creator selection.")
    print(f"  The form is not too long — it's confusing. Open-ended fields with no guidance.\n")
    print(f"  RECOMMENDED FIX:")
    print(f"  {FIX_RECOMMENDATIONS[worst_step]}")
    print(f"\n  Expected impact: +20–25pp Step 3→4 conversion.")
    print()


if __name__ == "__main__":
    run_analysis()
