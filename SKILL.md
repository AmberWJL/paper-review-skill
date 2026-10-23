---
name: paper-review
description: Read, understand, and critically review an academic research paper (AI/ML/CS by default) from a PDF, arXiv link, DOI, or title. Produces a fixed four-section review - Paper Overview, Champion (why accept), Adversary (why reject), Final Synthesis with verdict - grounded in the paper's actual figures, tables, and experiments, with venue/affiliation/history verified by web search. Use this whenever the user asks to review, critique, evaluate, assess, referee, steelman, red-team, or "read" a paper, asks "is this paper any good / worth reading / what do you think", shares an arXiv link or paper PDF and wants an opinion, or wants help preparing for reading-group or reviewer duty - even if they only ask for a "summary" of a paper. Do not use for turning a paper into slides (use paper-presentation) or for literature surveys across many papers.
---

# Paper Review: Champion vs Adversary

Produce a compact, consistent critical review of one paper. The review is not a summary: it
argues the strongest case *for* the paper, then the strongest case *against* it, from the same
evidence, and teaches the reader how to think about the paper.

## Workflow

### 1. Get the actual paper

Accept a PDF path, arXiv id/URL, DOI, or title. Resolve a link to a PDF (arXiv:
`https://arxiv.org/pdf/<id>`) and download it into its own empty directory. Read the real
PDF, including figures, tables, algorithms, and relevant appendices. The abstract and
introduction are marketing; the claims live in the tables.

Start with the map script so you know where things are before reading:

```bash
python3 -I scripts/paper_meta.py paper.pdf            # sections, figures, tables, arXiv id, venue hints, page numbers
python3 -I scripts/paper_meta.py paper.pdf --find "ablation|baseline|seed|standard deviation"
```

It is deterministic text extraction only (pdftotext or pypdf); it does no reasoning. Use its
page numbers to jump to the experiments, ablations, and appendix tables. Then read those
pages yourself, including the figure and table images when the renderer makes them available.

### 2. Verify context with web search

Search for: venue and year (preprint vs. accepted, which version), publication status, author
affiliations, the prior work the paper positions itself against, and any follow-ups or known
criticisms. Two or three searches are usually enough, and they belong in the same turn as the
review: run them, then write. Stopping after the searches leaves the user with nothing. Mark every fact from the PDF as `[paper]` and every
fact you confirmed by search as `[web]`; readers must be able to tell the difference, and the
paper itself may misdescribe its own status. Background you know but did not confirm this
session is neither: write it with "(unverified)" rather than borrowing the `[web]` tag. If search is unavailable, say so and label
the affected fields "from paper only, unverified".

### 3. Build the claim ledger (internal, not shown)

Before writing anything, list the paper's 2-4 major claims. For each, record:

- **Claim** as the authors state it (quote or close paraphrase).
- **Evidence** the paper actually provides, by location (Table 2, Figure 4, Section 5.3).
- **Assumptions** that bridge evidence to claim (e.g. "the benchmark reflects the real task",
  "baselines were tuned comparably", "gains at 1B hold at 70B").
- **Champion reading**: the most favorable fair interpretation.
- **Adversary challenge**: the strongest fair objection, and what evidence would resolve it.

Both sides of the review draw from this one ledger. That is what makes the two perspectives
honest: they disagree about interpretation and weight, not about what the paper contains.
Expose the ledger only if it materially clarifies the review (rarely).

### 4. Write the review

Use `references/output-template.md` exactly. Four main sections, nothing else. Target
1,500-2,500 prose words for a typical conference paper (tables, tags, and the metadata block do
not count); a long paper with several experiments may reasonably reach ~3,000. Compactness is a
feature: if over, drop the weakest criticism or reading-guide item rather than compressing the
five fields of a criticism you keep. Read
`references/validity-threats.md` before writing the Adversary section and
`references/ml-review-checklist.md` when deciding which experiments a paper in this subfield
is *expected* to have.

## Section guidance

**1. Paper Overview.** Metadata first (title, authors, affiliations, venue, year, area), then the
one-sentence contribution, problem, why it matters, core idea, method, main result. Explain the
method as a pipeline: Problem → limitation of prior work → key insight → proposed method →
evaluation → result. Add historical context that answers: what existed before, what gap this
fills, why it was interesting *at the time* (date the paper, not today). If the method is hard
to follow from prose, add one Mermaid flowchart or plain-text pipeline of at most ~8 nodes; skip
the diagram when the pipeline sentence already does the job.

**2. Champion.** Steelman, do not restate the abstract. Explain the method at two levels:
intuition (why could this work?) and technical (components, objective, training/inference,
datasets, baselines, evaluation protocol). Give a reading guide of 3-5 items (figure, table,
section) each with a reason. Name the strongest result, most important baseline comparison, most
informative ablation, and the main implication. If the paper has no formal ablation, use the
closest comparison that isolates a component and say so; if nothing isolates the novel part,
say that in one sentence, since it is Adversary material. End with "Strongest reason to accept".

**3. Adversary.** Act as a demanding senior reviewer. Start from the major claims: what evidence
would be required, what is provided, what assumptions connect them. First check the title and
abstract against the dependent variable: when the promised construct (retention, quality,
productivity, long-term outcomes) is never measured, that is the lead objection. For
observational and mining-software-repositories papers read the matching section of
`references/validity-threats.md`; the confounds there (group composition, outcome-defined groups,
post-outcome predictors, huge-N significance) carried a recent review. Organize criticisms by
construct, internal, and external validity (see `references/validity-threats.md`). For each
criticism give Concern, Evidence from the paper, Why it matters, Severity, and What would
resolve it. Prefer 2-4 deep criticisms over a checklist. End with "Strongest reason to reject",
whether it alone justifies rejection, and the smallest decisive experiment that would change
your mind.

**4. Final Synthesis.** Strongest Champion argument, strongest Adversary argument, the core
disagreement (usually: is the key assumption bridging evidence to claim reasonable?), verdict
and confidence, a 15-minute reading plan, and the one question to keep in mind while reading.

## Principles

1. Champion steelmans; Adversary stress-tests. Neither invents.
2. Both sides analyze the same core claims and the same evidence.
3. Substance only: no typos, grammar, formatting, or minor citation gaps. These never affect
   the verdict and crowd out real issues.
4. Distinguish fatal flaws (claim unsupported) from limitations (claim narrower than stated)
   from nice-to-haves (would strengthen an already-supported claim). Severity labels encode
   this; see calibration below.
5. Do not manufacture criticism to balance the Champion. A strong paper gets a short Adversary
   section and a confident Accept. Symmetry of effort, not of verdict.
6. Every criticism says why it matters *to the paper's conclusion*. "No error bars" is not a
   finding; "the 0.8-point gain in Table 2 is within the seed variance reported in Appendix C,
   so the main claim is unsupported" is.
7. Ground everything in specific sections, figures, tables, equations, experiments. Never
   invent a location: if you are unsure whether it was Table 3 or Table 4, say "the main
   results table (Section 5)". Before repeating a superlative ("strongest", "in every model",
   "all eight") verify it row by row in the cited table, and check whether a number counts
   entities (contributors, projects) or observations (patches, PRs); both have been wrong on a
   first draft.
8. Separate evidence from interpretation. "Table 2 shows +3.1 on GSM8K" is evidence; "this
   suggests the gain comes from the reward model" is interpretation. Write them as such.
9. Separate `[paper]` from `[web]`.
10. Teach how to think about the paper, not only whether it is good. The reading guide, the
    core disagreement, and the one question are the parts a reader keeps.

## Calibration

**Severity.** Minor: does not affect the main claim. Moderate: narrows or softens a claim.
Major: a main claim is weaker than stated or unsupported in an important regime. Fatal: a main
claim is unsupported, or a plausible confound fully explains the headline result.
Tie-break between two levels: take the higher one if the central claim depends on the affected
result, the lower one if the authors already scope the claim or the central claim rests on
other evidence. Several Moderate issues that compound (same claim, same direction) count as one
Major; unrelated Moderates stay Moderate.

**Verdict scale.** Strong Accept: novel, sound, important, and the Adversary found at most one
or two unrelated Moderate issues. Accept: sound and useful; Adversary issues are Moderate at
worst, possibly several. Weak Accept: real
contribution with one Major gap that does not undermine the central claim. Borderline: central
claim is plausible but the decisive experiment is missing. Weak Reject: one Major issue that
touches the central claim. Reject: central claim unsupported or a Fatal confound. Strong
Reject: central claim contradicted by the paper's own evidence or fundamentally unsound.

**Confidence.** High: you read the full paper including appendices and the critical evidence is
unambiguous. Medium: some tables/appendices were unreadable or the subfield's norms are
uncertain. Low: key material missing (no appendix, no code, figures unreadable) or outside
your expertise.

## On request, after the review

Keep the four sections stable; add these only when asked, as a short reply or an appendix.

- **"In simple words / what are we arguing?"** Restate each major objection as three plain
  sentences: what the authors claim, what was actually measured or compared, why the gap matters.
  Say what "hurts" or "significant" means in the paper's own units (acceptance odds, odds ratio).
- **"How would you do the study?" / "be a picky, mean reviewer."** Add *Redesign and
  overstatements*: (a) the design you would run, one paragraph per change (outcome that matches
  the title, unit of analysis, controls, pre-registered effect threshold, causal lever if any);
  (b) a bullet per overstatement quoting the paper's phrase and the table or definition that
  contradicts it; (c) the verdict that reviewer would give and the reframing that would earn an
  accept. Stay substantive: no cosmetic complaints.
- **"I'm the adversary / champion / presenting this."** The review still has all four sections;
  summarise the side they need in chat and point them to the `paper-presentation` skill, whose
  champion, adversary, and presenter modes build slides from this review's sections.

## Scope notes

- If the user explicitly wants only a summary, deliver Section 1 alone and offer the full
  review.
- Non-ML papers (systems, theory, HCI) use the same structure; adapt the checklist (proofs
  replace ablations, user studies replace benchmarks) and say which norms you applied.
- For a preprint, note that the status may change and date the review.
- Do not pad. If a subsection has nothing substantive, write one sentence saying so.
