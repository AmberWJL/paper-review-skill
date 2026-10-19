# What a paper in this subfield is expected to show

Use this to decide whether a missing experiment is a real gap (the community would expect it)
or a nice-to-have. Match the paper to the closest row; combine rows for hybrid papers.

| Paper type | Expected baselines | Expected ablations / analyses | Common failure modes |
|---|---|---|---|
| New architecture / layer | Strongest current architecture at matched params *and* matched FLOPs; a tuned vanilla baseline | Scaling curve (≥3 sizes), component ablation, throughput/memory | Gains vanish at scale; wins only on compute-mismatched comparison |
| Training objective / loss / RL recipe | Same model and data with the standard objective; the most recent comparable recipe | Ablation of each loss term, sensitivity to the key hyperparameter, multiple seeds | Baseline under-tuned; reward/judge hacking; unreported seed variance |
| Fine-tuning / alignment / preference learning (SFT, RLHF, DPO-style) | SFT-only, the standard preference method, same base model and same preference data | Data size curve, judge calibration vs humans, length-controlled win rates | Judge bias; gains only on one evaluator; preference data from a model that is also the judge |
| Prompting / inference-time method (CoT, decoding, test-time compute) | Matched-token or matched-call baseline (self-consistency at the same budget, best-of-N) | Cost vs accuracy curve; multiple model families; held-out task types | Compute-unmatched comparison; prompt tuned on test; single model family |
| Data / synthetic data / curation | Same model trained on equal-size real data; random-selection baseline | Contamination check; data size scaling; quality vs quantity decomposition | Test-set contamination via the generator model; conflating more data with better data |
| Efficiency (quantization, pruning, distillation, KV cache, serving) | Full-precision/full-size model; the strongest prior efficiency method at equal budget | Pareto curve (quality vs cost); hardware-measured latency not just FLOPs; worst-case tasks | Reporting theoretical speedups only; quality measured on easy benchmarks |
| Benchmark / dataset paper | Existing benchmarks on the same capability; human baseline | Inter-annotator agreement; contamination resistance; model ranking stability; error analysis | Saturation on release; label noise; no human ceiling; annotation protocol unreported |
| Agents / tool use / long-horizon | Strongest base model with simple ReAct-style scaffold; same tool budget | Success by task length; failure taxonomy; cost per task; reproducibility across runs | Environment-specific tricks; tiny task counts; no variance; benchmark built by the same authors |
| Interpretability / analysis | A null or random baseline for the claimed structure; alternative hypothesis | Causal intervention (ablate/patch), not just correlation; multiple models/layers | Correlational evidence presented as mechanism; cherry-picked examples |
| Theory with experiments | Assumptions stated and checked empirically where possible | Does the experiment test the regime the theorem covers? | Theorem assumptions never hold in the experiments; bound is vacuous |
| Systems / ML infrastructure | Production-grade prior system; well-tuned baseline configuration | Breakdown of where time/memory goes; scaling across hardware; end-to-end not microbenchmark | Comparing to an unoptimized baseline; benchmarking only the fast path |
| Safety / robustness / security | Adaptive attacker or strongest known attack; undefended baseline | Attack-success vs utility trade-off; transfer across models | Static attacks only; defense evaluated against attacks it was designed for |

## Cross-cutting expectations (recent ML venues)

- **Reproducibility:** code, seeds, hyperparameters, data splits. Absence is Moderate, not Major,
  unless the result depends on undisclosed details.
- **Statistical reporting:** multiple seeds or CIs when gains are < ~2x the typical seed
  variance on that benchmark.
- **Compute disclosure:** total compute for method and baselines; otherwise internal-validity
  threats cannot be ruled out.
- **Limitations section:** does it acknowledge the issues you found? Credit the authors when it
  does; the issue still counts, but honesty about scope lowers severity for external validity.
- **Dates matter:** judge novelty against what was public at the paper's submission date
  (`[web]`), not against today.
