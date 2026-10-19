# Output template

Use this structure verbatim. Four main sections only. Keep subsection labels as written so
reviews are comparable across papers. Mark facts as `[paper]` or `[web]` wherever the source
is not obvious from context (always for venue, year, status, affiliations, prior work); use
"(unverified)" for background you did not confirm by search.

---

# Review: <Paper title>

## 1. Paper Overview

| | |
|---|---|
| **Title** | ... |
| **Authors** | ... |
| **Affiliations** | ... `[paper]` / `[web]` |
| **Venue** | ... (accepted / preprint / under review; version reviewed) `[web]` |
| **Year** | ... |
| **Research area** | ... |
| **One-sentence contribution** | ... |

**Problem.** What is being solved. **Why it matters.** One or two sentences.

**Core idea.** The key insight in plain language.

**Method as a pipeline.**
Problem → limitation of prior work → key insight → proposed method → evaluation → result
(one line each, or a Mermaid/plain-text diagram of ≤8 nodes only if prose is insufficient).

**Main result.** The headline number(s) with location (Table/Figure) and the baseline they beat.

**Historical context.** `[web]` unless from the paper's related-work section.
- What existed before:
- Gap this paper fills:
- Why it was interesting at the time:

## 2. Champion — Why This Paper Should Be Accepted

**Intuition.** Why the key idea could work.

**Technical.** Components, objective/loss, training and inference procedure, datasets,
baselines, evaluation protocol. Cite equations/sections.

**Most important to read**
- Figure X — why
- Table Y — why
- Section Z — why
- (optional 1-2 more)

**Strongest experimental result.** ...
**Most important baseline comparison.** ...
**Most informative ablation.** ... (or the closest component-isolating comparison; say so if the paper has none)
**Main implication.** ...

**Strongest reason to accept:** one concise, substantive argument.

## 3. Adversary — Why This Paper Might Be Rejected

**Major claims and the evidence behind them.** For each of the 2-4 central claims: required
evidence / provided evidence / bridging assumptions. Keep this short; it is the spine of what
follows.

**Construct validity** (does the evaluation measure what is claimed?)
- **Concern:** ...
  **Evidence from the paper:** ...
  **Why it matters:** ...
  **Severity:** Minor / Moderate / Major / Fatal
  **What would resolve it:** ...

**Internal validity** (is the improvement attributable to the proposed method?)
- (same fields)

**External validity** (how far do the results generalize?)
- (same fields)

Omit a validity heading entirely if there is no substantive issue there and say so in one
sentence. Two to four deep criticisms total is the norm.

**Strongest reason to reject:** the most important scientific objection.
**Would this alone justify rejection?** Yes / Probably / Probably not / No
**What experiment would change my mind?** The smallest decisive experiment or analysis.

## 4. Final Synthesis

**Strongest Champion argument.** ...
**Strongest Adversary argument.** ...
**Core disagreement.** Usually: whether a specific bridging assumption is reasonable.

**Verdict:** Strong Accept / Accept / Weak Accept / Borderline / Weak Reject / Reject / Strong Reject
**Confidence:** High / Medium / Low (one clause on why)

**If I only have 15 minutes to read this paper**
1. ...
2. ...
3. ...
(3-5 ordered steps; sections, figures, tables)

**One question to keep in mind while reading:** ...
