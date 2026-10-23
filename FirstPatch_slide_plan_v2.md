# FirstPatch (adversary, v2) – 11-slide plan

**Paper:** From First Patch to Long-Term Contributor: Evaluating Onboarding Recommendations for OSS Newcomers, Turzo, Sultana, Bosu, IEEE TSE 51(4), 2025 (arXiv 2407.04159)
**Reference deck:** house style (references/visual-style.md); built fresh as FirstPatch_adversary_v2.pptx
**Palette:** slate blue 4A6FA5 · sage green 8FAF9A · light blue CFE3F0 · charcoal 2E3A46 · red E63946 · green 4CAF7A · grey 9AA5B1

**Role:** adversary, presented after the champions. Three points only. Points 1 and 2 answer the same sentence in the abstract and are presented together; point 3 gets a claim slide and two worked examples.

## 1. Paper summary
**Main idea:** The paper distils 15 task-related onboarding recommendations from 16 studies, maps each to one patch metric, and fits per-dataset logistic regressions (5 Gerrit projects, 3 GitHub activity strata) separately for newcomers and non-newcomers. It concludes that three recommendations should be abandoned after the first accepted patch "to increase their odds of becoming long-term contributors", and that four recommendations have "significant negative associations".

**Methodology:**
1. SLR: 605 papers to 16 primary studies (Table I); 15 recommendations (Table IV).
2. One metric per recommendation (Table V); acceptance (is_accepted) is the only outcome (Section IV-A-5).
3. Newcomer = no accepted patch yet; everyone else is one non-newcomer group (Section IV-A-4).
4. Two logistic regressions per dataset; odds ratios, Wald significance, explained deviance EP(%).
5. "Supported" if OR significant in the advised direction, "contradicted" if significant against it (Table XI).

**Findings used in the deck:**
| Metric | Value | Source |
|---|---|---|
| R6 change entropy OR, GitHub(H) | newcomers 0.85, non-newcomers 2.14 | Tables VIII, X |
| R7 doc-file ratio OR, LibreOffice | newcomers 4.56, non-newcomers 0.90 | Tables VII, IX |
| R9 log(delete) OR, GitHub(H) | newcomers 0.85, non-newcomers 1.11 | Tables VIII, X |
| Title / description metrics OR (significant ones) | 0.999 or 1.001 | Tables VII, VIII |
| EP(%) GitHub(H) newcomers | title len 0.01, desc len 0.22, title read 0.03, desc read 0.02, doc file 1.82, log(insert) 2.92 | Table VIII |
| Newcomers, GitHub(H) | 262,013 | Table VI |
| GFI OR, GitHub(H) newcomers | 5.57 | Table VIII |
| Bug fix supported | 7 of 8 datasets | Section IV-B |
| Gerrit data end | 30 April 2023 | Section IV-A-3 |

**Implications:** The newcomer-only associations and the GFI effect stand. The long-term-contributor advice rests on an unmeasured outcome and a confounded comparison, and the "four negative" recommendations are null effects that pass significance only because of sample size.

## 2. Outline
| # | Sentence | Visual type | Point |
|---|---|---|---|
| 1 | The adversary's case: the claims outrun the evidence | hero | – |
| 2 | I will raise three problems with the paper's claims | icon row (Morph source) | 1–3 |
| 3 | After your first accepted patch, the paper says to stop choosing simple tasks, documentation changes, and changes that delete few lines | three flip cards + quote | 1 |
| 4 | "Abandon", "increase their odds", and "long-term contributors" have no evidence behind them, because the study only measures whether a single patch was accepted | marked-up quote + four phrase cards | 1 |
| 5 | To earn that sentence, the outcome must be whether a contributor is still active a year after the first patch, not whether the next patch is accepted | two tracks: measured vs needed | 1 |
| 6 | Among non-newcomers, less experienced people tend to write the simple patches, so experience can explain the flip | confound triangle | 2 |
| 7 | Comparing people with the same experience would show whether stage or experience drives the flip | two designs side by side | 2 |
| 8 | The abstract reports four recommendations with "significant negative associations", and every one rests on an odds ratio of 0.999 or 1.001 | quote + four OR chips + EP chart | 3 |
| 9 | An odds ratio of 0.999 per word means ten extra words in a title move a 50% chance of acceptance to 49.75% | two PR titles + 50.0% vs 49.75% | 3 |
| 10 | It still passes p < 0.001 because with 262,013 newcomers almost any difference does, just as a coin landing heads 50.4% of the time looks "unfair" after 262,013 flips | coin analogy | 3 |
| 11 | The paper shows which patches get accepted, not which newcomers stay, so both claims should be rewritten before it is accepted | icon row with ✗ + rewritten claims | – |

Slide 6's sentence was softened from "comes mostly from" to "tend to come from" because the composition of the non-newcomer group is our hypothesis, not a measured fact.

## 3. Asset strategy (17 cropped images from the user's sheet + PowerPoint shapes)
| Slug | What | Reused on |
|---|---|---|
| hero-door | newcomer at an open door, corridor behind | 1 |
| thr-construct | balance scale (point 1) | 2–11 |
| thr-internal | two jars (point 2) | 2–11 |
| thr-conclusion | magnifier on a dot (point 3) | 2–11 |
| jar-nonnewcomers | mixed-bead jar alone | 6 |
| char-newcomer | newcomer with a patch | 5, 7 |
| char-maintainer | maintainer with a stamp | 6, 7 |
| char-employee | contributor with a lanyard | 6, 7 |
| icon-patch | patch document | 3, 5, 6, 9 |
| icon-stamp-accepted | green accepted stamp | 5, 6 |
| icon-sapling | sapling (long-term) | 5 |
| pt-experiment | flask (the fix) | 5, 7 |
| pt-holds | shield with check (still stands) | 11 |

Unused on the sheet but kept in assets/: jar-newcomers, icon-bug, icon-gfi-tag, icon-review-loop.

**Variants by overlay:** patch + small stamp = first accepted patch; patch ×3 offset = patches 2–10; strip icon at 65% transparency = not yet covered; red ✗ text shape on an icon = point closed.
**Shapes used as icons:** rounded rectangles (cards, chips, nodes, tiles, pills), rounded callouts (quotes), block arrows, connector lines with arrowheads (confound triangle), ovals (coin, legend dots), dashed divider, native bar chart.

## 4. Recurring motifs
**Tracker strip:** three slots at the bottom centre (y 6.55 in). On each content slide the current point's icon is the top-right badge and the other two sit in the strip, faded until covered; covered points keep their red ✗.
**Point icons with Morph:** slide 2 is the source. Badge: slides 3–5 scale, 6–7 jars, 8–10 magnifier. The ✗ is placed on the badge on the last slide of each point (5, 7, 10) so Morph carries it into the strip. Slide 11 returns all three to the agenda positions with their ✗.

## 5. Slides
### 1 · Title
Sentence: The adversary's case: the claims outrun the evidence
Main idea: this is a critique of scope, not of effort.
Visual: sentence left (36 pt), hero-door right, citation and "after the champions" in grey.
Animation: static. Transition to slide 2: Fade.

### 2 · Agenda
Sentence: I will raise three problems with the paper's claims
Main idea: three stops; the first two answer one sentence (said in the script, not shown).
Visual: scale, jars, magnifier at 1.8 in, centred columns; bold labels "No evidence", "Biased conclusion", "Significance from large samples", each with "Point N · <validity>" in grey beneath.
Animation: clicks 1–3 each icon and its labels Fade in turn.

### 3 · Point 1 · the claim
Sentence: After your first accepted patch, the paper says to stop choosing simple tasks, documentation changes, and changes that delete few lines
Main idea: this is the advice, and this is where it comes from.
Visual: three cards (R6, R7, R9) each with metric name, newcomer ✓ and non-newcomer ✗ with odds ratios and table source; footnote on OR direction; abstract sentence in a callout with source tag.
Animation: Morph in; click 1 cards Fade in sequence; click 2 checks Appear; click 3 crosses Appear; click 4 quote Wipe.

### 4 · Point 1 · the words
Sentence: "Abandon", "increase their odds", and "long-term contributors" have no evidence behind them, because the study only measures whether a single patch was accepted
Main idea: the sentence promises causation and a long-term outcome; the data hold one-patch correlations.
Visual: the abstract sentence at 20 pt with three phrases in red and "at non-newcomer status" in slate; four cards below in sentence order explaining each phrase.
Animation: click 1 quote Fade; click 2 phrases highlight in turn; clicks 3–6 cards Fly In from bottom.

### 5 · Point 1 · how it should be done
Sentence: To earn that sentence, the outcome must be whether a contributor is still active a year after the first patch, not whether the next patch is accepted
Main idea: measure retention; the data allow it.
Visual: top track "What the paper measured" (patch, arrow, stamp, "says nothing about who stays" in red); dashed divider; bottom track "What the claim needs" with flask (newcomer, first accepted patch, patches 2–10, sapling with "?"); data note on the Gerrit end date.
Animation: click 1 top track Wipe; click 2 red note Fade; click 3 bottom track Wipe step by step; click 4 sapling Pulse; click 5 data note Fade; click 6 ✗ on badge.

### 6 · Point 2 · the confound
Sentence: Among non-newcomers, less experienced people tend to write the simple patches, so experience can explain the flip
Main idea: one hidden cause produces the flip.
Visual: left mixed jar "non-newcomers, one pooled group"; centre triangle with maintainer and employee at "experience and trust", solid arrows to "complex, non-doc patch" and "accepted", dashed red arrow between them "what the regression sees"; right pills tenure ✗, affiliation ✗, author ✗.
Animation: Morph in; click 1 jar; click 2 characters Fly In; click 3 solid arrows Wipe; click 4 red dashed arrow Wipe; click 5 pills Fade, crosses Pulse.

### 7 · Point 2 · how to tell them apart
Sentence: Comparing people with the same experience would show whether stage or experience drives the flip
Main idea: two designs, and the result that would prove the adversary wrong.
Visual: left "Split non-newcomers by experience" with three bins (2–5, 6–20, core) and two outcome lines (green: flip already at 2–5, advice may hold; red: flip only in core, experience explains it); right "Follow the same person" with nine simple/complex tiles; footer on adding tenure, affiliation, author effects.
Animation: click 1 bins Fade; clicks 2–3 outcome lines; click 4 right side Wipe; click 5 explanation; click 6 ✗ on badge.

### 8 · Point 3 · the claim
Sentence: The abstract reports four recommendations with "significant negative associations", and every one rests on an odds ratio of 0.999 or 1.001
Main idea: the "negative" third of the headline is four near-1.0 odds ratios.
Visual: abstract quote; 2×2 chips R10–R13 each 0.999*** with dataset; native bar chart of EP(%) for GitHub(H) newcomers (four grey bars beside doc file and log(insert) in slate); caption "at most 0.22%".
Animation: Morph in; click 1 quote; click 2 chips Zoom; click 3 chart Wipe from bottom; click 4 caption.

### 9 · Point 3 · example 1
Sentence: An odds ratio of 0.999 per word means ten extra words in a title move a 50% chance of acceptance to 49.75%
Main idea: in practice the effect is a quarter of a percentage point.
Visual: 5-word and 15-word pull-request titles; 50.0% (grey) to 49.75% (red); working "odds × 0.999¹⁰ = 0.990"; rounding range 49.6–49.9%.
Animation: click 1 short title; click 2 long title; click 3 50.0%; click 4 arrow + 49.75%; click 5 working box.

### 10 · Point 3 · example 2
Sentence: It still passes p < 0.001 because with 262,013 newcomers almost any difference does, just as a coin landing heads 50.4% of the time looks "unfair" after 262,013 flips
Main idea: significance at this N says nothing about importance.
Visual: coin (two ovals, "H"), "262,013 flips · 50.4% heads"; "p ≈ 0.00004" in red; "= 262,013 newcomers in GitHub(H)"; banner "significant is not the same as important".
Animation: click 1 coin Spin; click 2 labels; click 3 p-value Grow & Turn; click 4 equals + N; click 5 banner Wipe; click 6 ✗ on badge.

### 11 · Conclusion
Sentence: The paper shows which patches get accepted, not which newcomers stay, so both claims should be rewritten before it is accepted
Main idea: reject as written; the fix is rewording what the data support.
Visual: three icons back in the row with ✗; Claim 1 box (struck original phrase, rewritten claim); Claim 2 box (struck "four indicate significant negative associations", rewritten "no practical effect"); shield line "Still stands: GFI 5.57×, bug fixes 7 of 8".
Animation: Morph in; click 1 crosses Pulse; click 2 Claim 1 box; click 3 Claim 2 box; click 4 still-stands line.

**Cleanup pass:** badge labels, source and dataset tags, footnotes, and captions that repeat the sentence were removed from every slide. Their content now lives in the speaker notes, which hold a full talking script per slide with [click] cues and an IF ASKED list of backup facts.

## 6. Morph setup notes
Already done in the file: slides 3–11 carry Transition → Morph (0.8 s, Fade fallback); slide 2 carries Fade. The Morph objects are pictures named `thr-construct`, `thr-internal`, `thr-conclusion` and text shapes named `mark-thr-construct`, `mark-thr-internal`, `mark-thr-conclusion`, plus `badge-label`. Every other object has a per-slide name (`s5-…`) so Morph does not pair unrelated shapes. If you replace an icon, paste the new picture and give it the same name in the Selection Pane on every slide; Morph only moves objects with matching names. Per-object click animations are not set; add them from the speaker notes.

## 7. Native charts
8: column chart, EP(%) GitHub(H) newcomers (Table VIII): title length 0.01, description length 0.22, title readability 0.03, description readability 0.02, doc file 1.82, log(insert) 2.92; first four bars grey 9AA5B1, last two slate 4A6FA5; labels "0.00".

## 8. Image-generation prompts (0 required, 2 optional)
**Icon suffix:** flat cartoon icon, thick charcoal #2E3A46 outlines, fills in slate blue #4A6FA5, sage green #8FAF9A, light blue #CFE3F0, transparent PNG, square, centred, no text, no letters, no numbers.
**Character suffix:** flat cartoon character, thick charcoal #2E3A46 outlines, palette slate blue #4A6FA5, sage green #8FAF9A, light blue #CFE3F0, transparent PNG, no text.

All assets in use are already on the user's sheet. Optional upgrades:
1. **icon-coin** — a single coin seen face-on, simple raised rim, slate blue face. + icon suffix (replaces the two ovals on slide 10)
2. **icon-patch-stack** — three patch documents fanned out, slightly offset. + icon suffix (replaces the three overlaid patches on slide 5)

**Batch tips:** generate against the existing sheet as a style reference so outline weight matches; transparent PNG at 1024×1024.
