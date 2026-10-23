# Review: From First Patch to Long-Term Contributor: Evaluating Onboarding Recommendations for OSS Newcomers

*Example output of the paper-review skill for an empirical software-engineering (mining-software-repositories) paper. Reviewed 2026-10-20 from the IEEE Xplore version. Facts from the PDF are marked `[paper]`; facts confirmed by search are marked `[web]`.*

## 1. Paper Overview

| | |
|---|---|
| **Title** | From First Patch to Long-Term Contributor: Evaluating Onboarding Recommendations for OSS Newcomers |
| **Authors** | Asif Kamal Turzo, Sayma Sultana, Amiangshu Bosu |
| **Affiliations** | Department of Computer Science, Wayne State University, Detroit `[paper]`; Bosu leads the SEAL lab there `[web]` |
| **Venue** | IEEE Transactions on Software Engineering, vol. 51, no. 4, pp. 1303–1318; received July 2024, accepted March 2025 `[paper]`, confirmed `[web]`. Also arXiv 2407.04159 and a journal-first presentation at FSE 2026 `[web]` |
| **Year** | 2025 |
| **Research area** | Empirical software engineering; OSS onboarding and code review |
| **One-sentence contribution** | A systematic literature review distils 15 task-related onboarding recommendations, and logistic regression over 1.4M Gerrit code reviews and 6M GitHub pull requests tests which of them actually correlate with first-patch acceptance, and whether they still hold once a contributor is no longer a newcomer. |

**Problem.** OSS projects depend on converting first-time contributors into long-term ones, but most onboarding advice comes from interviews or small samples, so nobody knows whether it generalises across projects or whether it keeps helping after the first patch is accepted `[paper]`.

**Why it matters.** Following advice that is wrong for your project, or that stops applying after you are no longer new, could actively hurt a contributor's chances. Projects also invest in GFI labelling and mentoring on the assumption these recommendations work.

**Core idea.** Treat each recommendation as a testable hypothesis: map it to a measurable property of a patch (size, bug-fix label, documentation ratio, title readability, iterations, promptness), then ask whether compliance predicts acceptance, separately for newcomers and non-newcomers, in eight different contexts.

**Method as a pipeline.**
Problem: onboarding advice is unvalidated and context-free → Limitation of prior work: qualitative, few projects, newcomer-only → Key insight: recommendations can be operationalised as patch attributes and tested at scale against acceptance → Method: SLR (605 → 16 primary studies, Table I) yields 15 recommendations (Table IV); each mapped to a metric (Table V); inferential multivariate logistic regression per dataset following Harrell, with variable clustering for multicollinearity, odds ratios (OR), and per-variable explained deviance EP(%) → Evaluation: 5 Gerrit projects (Android, LibreOffice, oVirt, Typo3, Wikimedia) and 3 GitHub strata (1,155 projects split by PR volume), two models each (newcomer, non-newcomer), Table VI → Result: Tables VII–XI.

**Main result.** No recommendation is supported in all eight datasets `[paper]`. For newcomers, working on bug fixes (R4) and adding fewer lines (R8) are supported in 7 of 8; GFIs (R2) have the largest single effect (OR 5.57 in high-activity GitHub, Table VIII); title and description length/readability (R10–R13) are "significantly negative" but with explanatory power under 0.2%. Three recommendations (low complexity R6, documentation R7, fewer deletions R9) flip sign for non-newcomers (Table XI), which the authors read as advice to abandon after the first accepted patch.

**Historical context.**
- *What existed before* `[web]` and the paper's Section II: Steinmacher et al.'s barrier catalogues and onboarding guidelines (2015–2018) from interviews and surveys; Tan et al. (FSE 2020) characterised Good First Issues on GitHub; GFI recommender tools followed (Xiao et al. ICSE 2022, GFI-Bot). The 16 primary studies are mostly interview/survey based; only five are quantitative and those focus on GFIs (Table III) `[paper]`.
- *Gap this paper fills*: a large-scale, multi-platform test of the whole recommendation list, and the first newcomer vs. non-newcomer comparison `[paper]`.
- *Why it was interesting at the time*: by 2024 GFI labelling and newcomer programmes were standard practice, OSS sustainability was a live concern, and the advice underpinning them had never been checked against acceptance data across contexts (unverified beyond the paper's own framing).

## 2. Champion — Why This Paper Should Be Accepted

**Intuition.** Onboarding advice is folk wisdom accumulated from a handful of projects. If it is real, it should leave a statistical fingerprint: patches that follow it should be accepted more often, everywhere. If the fingerprint is absent or reverses between projects, the advice is at best local. Testing that at scale is cheap relative to its practical value, and nobody had done it.

**Technical.** Stage 1 is a Kitchenham-style SLR with hybrid search, forward/backward snowballing, expert validation, and two-author extraction with card sorting (Section III-A). Stage 2 maps each of the 15 recommendations to one attribute (Table V), with prior-validated metrics where available: total churn and change entropy from the defect-prediction literature, Flesch reading ease for titles and descriptions, promptness and patchset count from code-review studies. Datasets are large and separately modelled (Table VI). Models are inferential logistic regressions following Harrell: Spearman-based variable clustering at |ρ| = 0.7 drops redundant predictors (churn, file count), log transforms for skewed variables, Veall–Zimmerman pseudo-R², likelihood-ratio tests against null, and a per-variable EP(%) deviance contribution that acts as an ablation (Section IV-A-5). A recommendation is "supported" in a dataset if its attribute has a significant positive OR. The replication package is public `[paper]`.

**Most important to read**
- Table IV — the 15 recommendations with their rationale and sources; this is the object being tested, and it shows how thin the evidence base was (R10–R11 rest on two GFI studies).
- Table V — the metric mapping. Every construct-validity judgement about the paper lives here.
- Tables VII and VIII, EP(%) columns — the newcomer results. Reading the odds ratios alone misleads; EP tells you which effects matter.
- Table XI — the one-page summary of support/contradiction across all 16 models; it is the paper's actual finding.
- Section IV-A-5 and the "Power of each variable" paragraph — how "supported" is defined and how EP is computed.

**Strongest experimental result.** The GFI effect: for newcomers in high-activity GitHub projects, a GFI-labelled issue raises acceptance odds 5.57× (Table VIII), compared with 2.05× for non-newcomers (Table X). That is a large, newcomer-amplified effect in the stratum where it matters most, and it validates the GFI practice directly.

**Most important baseline comparison.** There is no competing model; the key comparison is newcomer vs. non-newcomer regressions on the same datasets (Tables VII/VIII vs. IX/X), summarised in Table XI. The secondary comparison with Tan et al. (Section V-B) explains why their GFI-only findings on description length and deletions differ from this paper's.

**Most informative ablation.** The EP(%) analysis. It shows that review iterations (R15) dominate in three of the five Gerrit newcomer models (14% of explained deviance in oVirt, 11% in LibreOffice, 9% in Typo3), while title/description metrics explain essentially nothing, which is what lets the authors downgrade R10–R13 despite their stars.

**Main implication.** Onboarding advice is context-dependent and partly stage-dependent. Projects should keep investing in GFI labelling and steer newcomers toward bug fixes and small insertions, and newcomers should not spend effort polishing titles.

**Strongest reason to accept:** It is the first study to put the entire catalogue of task-related onboarding advice through a uniform, large-scale, multi-platform test, and its most useful outputs are negative: several widely repeated recommendations have no practical effect, and none generalises everywhere. That is exactly the correction the onboarding literature needed, delivered with a public dataset.

## 3. Adversary — Why This Paper Might Be Rejected

**Major claims and the evidence behind them.**
- *C1: Four recommendations help newcomers in most contexts; four are context-dependent; four are negative.* Evidence: Tables VII–VIII. Bridging assumptions: a significant OR is a meaningful effect; the association reflects the recommendation rather than who submits such patches.
- *C2: Three recommendations are newcomer-specific and should be abandoned at non-newcomer status "to increase the odds of becoming long-term contributors"* (abstract, title, Conclusion). Evidence: sign flips between Tables VII–VIII and IX–X. Bridging assumptions: non-newcomer patch acceptance is a proxy for long-term contribution; the non-newcomer population is comparable to a newcomer one patch later; correlations can be read as advice.

**Construct validity**
- **Concern:** The title and the headline advice are about becoming a long-term contributor, but nothing in the paper measures retention, tenure, or continued contribution. The RQ3 dependent variable is acceptance of a non-newcomer's patch.
  **Evidence from the paper:** Section IV-A-4 defines newcomer as "until first CR/PR accepted"; everyone else is one undifferentiated control group. The abstract and Conclusion nonetheless state that abandoning R6, R7, R9 raises "the odds of becoming long-term contributors". Section VI concedes non-newcomers are diverse but only as a conclusion-validity note.
  **Why it matters:** The paper's distinctive claim, the one in its title, is a claim about a construct it never operationalised. What is shown is that patches from established contributors are accepted under different conditions than patches from newcomers.
  **Severity:** Major.
  **What would resolve it:** A survival or retention analysis: among contributors with one accepted patch, does the complexity/documentation profile of their next k patches predict still contributing 12 months later?

**Internal validity**
- **Concern:** The sign flips underpinning C2 are most simply explained by population composition, not by a strategy change. Non-newcomers include core developers and, in Android, oVirt and Wikimedia, employees of the sponsoring organisation; those people are both trusted and assigned complex, non-documentation work. Their complex patches are accepted because of who they are, not because complexity helps.
  **Evidence from the paper:** No control for affiliation, tenure, prior accepted count, or author identity; no project fixed effects within the pooled GitHub strata of 385 projects each; standard errors are not clustered by author, so one prolific non-newcomer contributes hundreds of correlated observations. Section VI names heterogeneity only as a threat to grouping.
  **Why it matters:** "If the claimed contribution were removed, could something else explain the result?" Yes: selection into complex work by trusted contributors fully explains R6/R7/R9 reversing sign for non-newcomers without implying that a second-patch contributor should pick harder tasks.
  **Severity:** Major for C2; it does not touch the newcomer-only associations in C1.
  **What would resolve it:** A within-person design: follow the same contributors from patch 2 to patch 10 and compare acceptance of their own complex vs. simple patches, or at minimum add tenure and affiliation covariates and author-clustered errors.

- **Concern:** The two task-completion recommendations, R14 promptness and R15 iterations, are measured after submission and are partly outcomes of the review rather than newcomer behaviours. A patch that is abandoned or rejected outright gets one patchset and no author delay to measure; a patch reviewers engage with accumulates iterations.
  **Evidence from the paper:** Table V defines iterations as total patchsets and promptness as inverse author delay. Iterations are the strongest predictor in three of the five Gerrit newcomer models (EP 8.8–14.2%, Table VII), far above any task-selection variable; in Wikimedia promptness, also post-submission, is the strongest.
  **Why it matters:** The best-explaining variables in the models may be reverse-causal, which inflates pseudo-R² and underwrites Key Takeaway 4's advice to "be patient". The task-selection claims are less affected because they are fixed at submission time.
  **Severity:** Moderate for the paper overall, Major for R14/R15 specifically.
  **What would resolve it:** Re-fit on patches that received at least one review round, or measure promptness only on the first requested revision.

- **Concern:** Support and contradiction are decided by p-values on datasets of 10⁴–10⁶ patches, so practically null effects count as findings.
  **Evidence from the paper:** Title length and description length are "significant" at p < 0.001 with OR 0.999 or 1.001 (Tables VII, VIII, X). The text acknowledges EP < 0.2%, yet the abstract still reports "four indicate significant negative associations", and Table XI marks them with red crosses.
  **Why it matters:** The "four negative" third of the headline result is a statistical artefact of sample size. The honest reading is "no effect", which is a different and more useful message.
  **Severity:** Moderate, since the authors supply the EP evidence to see through it, but the abstract and Table XI do not apply it.
  **What would resolve it:** A minimum effect-size criterion for "supported/contradicted" (for example OR per standard deviation outside 0.9–1.1) applied uniformly.

**External validity.** The eight datasets are a genuine advance on prior work, and the context dependence found is itself the finding, so there is no substantive generalisation problem beyond the usual caveats: top-10 languages only, Gerrit projects are all large and mature, and GFI could only be tested on GitHub.

**Strongest reason to reject:** The paper's title and its most-quoted advice rest on a construct it never measured and on a comparison between two populations that differ in who they are, not just in what stage they are at. "Abandon R6, R7, R9 to become a long-term contributor" is not supported; "established contributors' complex patches get accepted" is.

**Would this alone justify rejection?** Probably not. The newcomer-only results (RQ1, RQ2) stand with caveats and the dataset is valuable; the fix for C2 is mostly reframing, and TSE reviewers evidently accepted it in this form.

**What experiment would change my mind?** A within-contributor analysis of patches 2–10 showing that, for the same early-stage contributors, moving to more complex or non-documentation changes is associated with higher acceptance and with continued activity a year later.

## 4. Final Synthesis

**Strongest Champion argument.** A uniform, large-scale test across eight contexts shows that no onboarding recommendation generalises everywhere and that several popular ones have no practical effect, while GFIs and bug fixes clearly help newcomers. This is a needed empirical correction with a public replication package.

**Strongest Adversary argument.** The "long-term contributor" framing is unmeasured, and the newcomer vs. non-newcomer sign flips are explained by who non-newcomers are rather than by what a newcomer should do next, so the paper's distinctive advice is interpretation, not evidence.

**Core disagreement.** Whether a difference in correlational structure between two differently composed populations licenses a stage-based recommendation to individuals. The Champion treats the flip as informative about stage; the Adversary treats it as informative about selection.

**Verdict:** Weak Accept
**Confidence:** High. The full paper is readable, the statistical design is fully described, and the issues are visible in the paper's own tables; I did not inspect the replication package.

**If I only have 15 minutes to read this paper**
1. Abstract, then Table IV, to see exactly which 15 claims are being tested (3 min).
2. Table V, asking for each row whether the metric really measures the recommendation (3 min).
3. Table XI, then the EP(%) columns of Tables VII and VIII, ignoring any OR within 0.99–1.01 (5 min).
4. Section IV-A-4 (newcomer definition) and the "supported" definition in IV-A-5 (2 min).
5. The Conclusion's final sentence against Section VI, and decide for yourself whether "long-term contributor" was measured (2 min).

**One question to keep in mind while reading:** When a recommendation's correlation flips sign between newcomers and non-newcomers, is that telling a newcomer what to do next, or just describing who the non-newcomers are?

---

*Follow-ups requested after this review, showing the on-request extensions:* the three objections restated in plain words (claim → what was measured → why the gap matters); a "redesign and overstatements" appendix (within-person design, retention outcome, tenure/affiliation controls, effect-size threshold; abstract counting 15 evaluated recommendations when two were dropped for multicollinearity, "four negative" resting on OR 0.999, "1,155 projects" being three pooled regressions); and a hand-off to the presentation skill's adversary mode.
