# Froker Business Onboarding Drop-off Analyzer

Identifies the exact onboarding step where local businesses abandon the platform, compares completers vs droppers, and outputs one actionable fix per drop-off point.

> Built Aug 2024 – Aug 2025 — pure Python + synthetic data. PM-focused analysis: not just where the drop is, but why and what to change.

---

## Problem

Local businesses sign up on the platform to run creator campaigns, but most never post their first campaign. The team knew activation was low but didn't know **which step** was the problem — so every proposed fix was a guess.

---

## Onboarding Steps

```
Step 1: Business signup       (name, category, phone)
Step 2: Business profile      (description, logo, hours)
Step 3: Campaign brief        (what do you want creators to post?)
Step 4: Creator selection     (pick from recommended creators)
Step 5: First campaign live   (deal confirmed with a creator)
```

---

## Key Finding (from demo data)

```
Step                          Reached  Conv%   Drop%   Avg min
Step 1 — Signup                  150  100.0%    0.0%      3.4m
Step 2 — Business Profile        123   82.0%   18.0%      8.1m
Step 3 — Campaign Brief           54   36.0%   56.1%  ← WORST   18.2m
Step 4 — Creator Selection        42   28.0%   22.2%      6.1m
Step 5 — Campaign Live            38   25.3%    9.5%      2.0m
```

**56% of businesses that complete their profile drop off at the campaign brief step.**

Time signal: Businesses that reach the brief step spend **18+ minutes** on it on average. The form is not too long — it's an open text field with no guidance. Small business owners don't know what a "campaign brief" is.

**Recommended fix:** Replace the open-form brief with a 5-question wizard + example prompts per business category.
- *"What should creators do?"* → multiple choice: Visit & Review / Show Product / Attend Event / Other
- *"What's your goal?"* → Footfall / Followers / Awareness
- *"Describe your vibe in 3 words"* → text, max 3 words
- Auto-generate draft brief from answers

Expected impact: +20–25pp Step 3→4 conversion.

---

## Files

| File | Description |
|---|---|
| `onboarding_analyzer.py` | Full step analysis, time-spent, exit rates, fix recommendations |
| `requirements.txt` | Dependencies |

---

## Run locally

```bash
pip install -r requirements.txt
python onboarding_analyzer.py
```

---

## Design Decisions

| Decision | Reasoning |
|---|---|
| Time-spent per step alongside exit rate | Exit rate alone is misleading — a step with 10% exit but 45 min avg time is worse than a step with 20% exit at 2 min |
| Fix recommendation per step | Data analysis without a recommended action is a report, not a PM deliverable |
| Completer vs dropper comparison | Shows what behaviour differs between the two groups — not just where they stop |
