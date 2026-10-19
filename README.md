# paper-review

An [Agent Skill](https://agentskills.io) for reading, understanding, and critically reviewing
academic research papers (AI/ML/CS by default). Works with Claude Code, Claude.ai, and other
agents that load the `SKILL.md` format.

Given a PDF, arXiv link, DOI, or title, it produces a fixed four-section review:

1. **Paper Overview** – metadata, problem, core idea, method as a pipeline, main result, and
   historical context (venue, affiliations, and prior work verified by web search and labelled
   `[paper]` vs `[web]`).
2. **Champion** – the strongest case for acceptance: intuition and technical explanation, a
   reading guide to the key figures/tables/sections, strongest result, key baseline, key
   ablation, main implication.
3. **Adversary** – a demanding senior reviewer's case for rejection, organised by construct,
   internal, and external validity; each criticism gives evidence, why it matters, a severity
   (Minor/Moderate/Major/Fatal), and what would resolve it.
4. **Final Synthesis** – the core disagreement, a verdict and confidence, a 15-minute reading
   plan, and one question to keep in mind while reading.

It steelmans and stress-tests the *same* claims and evidence, ignores cosmetic issues, and does
not manufacture criticism for symmetry.

## Install

- **Claude Code**: copy this folder to `.claude/skills/paper-review/` (project) or
  `~/.claude/skills/paper-review/` (global), or download `paper-review.skill` from Releases and
  save it.
- **Other agents**: point your skills loader at this folder.

## Layout

```
SKILL.md                         workflow, principles, calibration rules
references/output-template.md    the four-section review layout
references/validity-threats.md   construct / internal / external validity checklists
references/ml-review-checklist.md  expected baselines and ablations per paper type
scripts/paper_meta.py            deterministic PDF map: sections, figures, tables, theorems,
                                 arXiv id, venue hints, page numbers (no reasoning)
evals/evals.json                 sample test prompts
```

The script needs `pdftotext` (poppler) on PATH or `pip install pypdf`:

```bash
python3 -I scripts/paper_meta.py paper.pdf
python3 -I scripts/paper_meta.py paper.pdf --find "ablation|seed"
```

## Example

Prompt: *"Can you review this paper for me? I'm presenting it at our reading group next week
and want to know how much to trust the claims."* with the DPO paper (arXiv 2305.18290) yields a
~2,500-word review ending in **Accept / High confidence**, with the Adversary's strongest
objection being that the real-data evidence (single runs, GPT-4-only dialogue judge, ≤6B) is
thinner than the theory.
