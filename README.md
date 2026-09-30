🇩🇪 [Deutsche Version](README_DE.md)

# UC2 — Evaluation Harness for Ticket Classification

## Problem

[UC1](https://github.com/JulianStnDev/ai-uc-01-ticket-classification) produced a classifier that sorts support tickets by `category`, `urgency` and `sentiment`. It was checked against 6 sample tickets. With n=6, though, there is no way to tell whether the prompt actually works or whether the six examples just happened to fit — let alone whether a prompt change is an improvement or merely shifts the errors around.

This repo builds the measurement setup for that: a Goldset of 73 hand-labeled support tickets from a fictional productivity app (FocusFlow) and a harness that measures every prompt version against it — with a confusion matrix, error direction and cost per run.

The audience is the person who has to decide whether a changed prompt may go to production.

## PM Decision

**Accuracy alone is not enough.** For `urgency`, the two error directions have different costs: an underestimated ticket sits unattended, an overestimated one creates an unnecessary escalation. A single combined hit rate hides exactly this difference. The harness therefore reports underestimation and overestimation separately, with ticket IDs, and reports `category` as a full 5×5 matrix instead of a single percentage.

**Running and scoring are separate.** `score.py` first writes all raw results to `evals/predictions_<tag>.csv` and then computes the metrics from that file. With `--from-cache`, the scoring can be reworked as often as needed without paying for the API again. Every run carries a tag, so older measurements are preserved and remain comparable.

**The Goldset is labeled by hand**, not by a model. A model-labeled Goldset measures the agreement between two models, not quality against the domain intent.

**The classifier started out byte-identical to UC1.** Only after the baseline had been measured was the prompt deliberately changed — with an explicit note that UC1 is therefore no longer at the same state. The reasoning is in [docs/decisions.md](docs/decisions.md).

## Architecture Sketch

```
  evals/goldset.csv                    classify.py
  73 tickets, 3 labels                 1 Messages call per ticket
         │                             tool_choice forces classify_ticket
         │                             3 enum fields, Haiku 4.5
         │                                     │
         └──────────────┬──────────────────────┘
                        ▼
                    score.py
         ┌──────────────┴──────────────┐
    Phase 1: Run               Phase 2: Scoring
    ThreadPool, --workers N    reads predictions_<tag>.csv
         │                             │
         ▼                             ▼
  predictions_<tag>.csv        Confusion matrix, P/R/F1,
  run_meta_<tag>.json          error direction, cost, latency
                                       │
                                       ▼
                               results_<tag>.md
```

No framework, directly against the Anthropic SDK. Classification uses forced tool use (`tool_choice`) so that the response comes back schema-valid and no parsing is needed. All of the domain logic lives in the `description` fields of the three enums — that is the lever on which the three versions below differ.

## Evaluation Results

n=73, measured serially (`--workers 1`), model `claude-haiku-4-5`, one run per version.

| Metric | Baseline (= UC1) | v2 | v3 |
|---|---:|---:|---:|
| **Category accuracy** | 82.2% | 86.3% | **89.0%** |
| Macro-F1 | 0.801 | 0.858 | **0.889** |
| **Urgency accuracy** | 71.2% | 68.5% | **79.5%** |
| — underestimated (ticket sits unattended) | 7 | 14 | **8** |
| — overestimated (unnecessary escalation) | 14 | 9 | **7** |
| **Sentiment accuracy** | 68.5% | **86.3%** | 84.9% |
| Cost / 1000 requests | $1.38 | $1.86 | $2.23 |
| Median latency | 0.87s | 0.90s | 0.92s |

### How It Got There

**The baseline exposed three calibration gaps** that had remained invisible at n=6. The most striking: `other` had a recall of 0.43 — the category was described as "alles andere" (everything else), while the other four named concrete conditions. A category without a positive feature loses every head-to-head against one that has them. On top of that came an overly broad urgency rule ("explizite Zeitangabe **oder** Frist" (explicit time reference **or** deadline)), which read any time reference in the text as a deadline, and a sentiment definition that only triggered on an angry tone and classified matter-of-factly worded damage reports as neutral.

**v2 fixed all three** — and raised sentiment from 68.5% to 86.3% without making a single ticket worse. At the same time, **urgency dropped to 68.5%**. The cause was revealing: the tightened deadline rule removed a crutch that tickets had been relying on unnoticed until then. Four tickets that the baseline had correctly identified as `high` had never been classified via the condition "Kernfunktion unbenutzbar" (core function unusable), but via the loose time reference. Most clearly with a ticket in which the app crashes right at startup — a textbook case of "Kernfunktion unbenutzbar", and the rule still did not apply. In addition, it turned out that **no rule existed at all** for money already lost: the Goldset rated such tickets as `high`, but the enum description did not know this case.

**v3 targeted exactly that**: concrete examples of "Kernfunktion unbenutzbar" and a new, deliberately narrow condition for financial damage that has already occurred and is quantified. Result: 9 tickets fixed, 1 newly wrong — and overestimation did **not** come back; instead it fell to 7 cases, the lowest value of all three runs.

### Known Limitations

**Four `high` tickets are still underestimated.** For two of them, this is the deliberately chosen price of the narrow wording: they describe financial damage that has occurred but do not state an amount, and the rule requires a figure. Loosening it would very likely bring back the over-escalation that v3 just eliminated. A third ticket (*"passwort funktioniert nicht mehr"* (password no longer works)) literally falls under "Login dauerhaft nicht möglich" (login permanently impossible) and still ends up as `medium` — there is no explanation for this so far.

**Two `billing`/`other` edge cases remain open.** The boundary rule ("konkrete Transaktion im eigenen Vertrag" (specific transaction in the user's own contract) vs. "allgemeine Kritik am Preisniveau" (general criticism of the price level)) clearly assigns a complaint about a price increase to `billing` — the model still picks `other`. A request for education discounts goes the wrong way for the same reason. These two tickets are the entire remaining `billing` weakness (recall 0.85).

**One sentiment class is too thin.** `positive` occurs only twice in the Goldset. Sentiment accuracy says practically nothing about this class; `score.py` now automatically warns about classes below n=5.

**20 convergent contradictions across 15 tickets remain.** These are the cases in which the classifier (Haiku) and the Goldset auditor (Sonnet) independently deviate from the Goldset in the same direction — spread across 9 urgency, 8 sentiment and 3 category judgments. Two independent models with the same deviation are a stronger signal than a single one, and this list would have been the next sensible starting point: either as a label correction or as a further rule refinement.

It is deliberately not pursued further. The reason is the course of the three rounds: v2 → v3 brought clear, explainable gains (sentiment +17.8pp with zero regressions, then urgency +11.0pp), whereas the v4 round cost more schema and money, fixed not a single real classifier error, and through the coupling effect knocked 5.4 points off elsewhere. That is the point where the marginal return tips — every further refinement lengthens the schema, raises costs and quite likely shifts errors instead of eliminating them. With n=73 and one run per version, a gain of one or two tickets could no longer be distinguished from noise anyway.

The list is therefore not worked through but documented: `evals/goldset_audit_v3.md` contains all 44 candidates with reasoning. The audit is meant as a tool to be re-run when needed — not as a task list that has to be ticked off.

## Cost & Latency

- **Cost per 1000 requests: $2.23** (avg. 1886 input / 68 output tokens, Haiku 4.5 at $1/$5 per million tokens)
- **Median latency: 0.92s** ¹
- **Quality metric: 89.0% category accuracy** (Macro-F1 0.889)

¹ Deliberately the median instead of p95. At n=73, the 95th percentile sits at rank 70, so a single outlier has full impact — in the v3 run one request took 7.03s and raised p95 to 1.90s, while the median stayed unchanged at 0.92s. A p95 figure would be false precision at this sample size.

### Cost vs. Quality

All of the domain logic lives in the enum descriptions, and these are sent again with every request. Over the three versions, the schema grew from 1180 to 3344 characters and the input tokens from 1036 to 1886 — with an average ticket of a few dozen tokens, the schema thus accounts for by far the largest share of the cost.

| | Baseline → v3 |
|---|---|
| Cost | **+62%** |
| Category accuracy | +6.8pp |
| Urgency accuracy | +8.3pp |
| Sentiment accuracy | +16.4pp |

Whether this trade-off pays off depends on the use case: at 100,000 tickets per month, that is $223 instead of $138. An untested lever is prompt caching — it would hit exactly the schema portion, but it requires a minimum length of the cached prefix that has not yet been verified.

## Learnings

**Three fields in one tool call are not independent of each other.** In v3, only `category` and `urgency` were changed — sentiment accuracy still fell by 1.4pp (3 tickets fixed, 4 newly wrong). All three values are produced in the same response; a change to one description can shift the output of the others along with it. Practical consequence: the three metrics cannot be optimized separately, and a single run is not enough to distinguish 1–2pp from noise.

**A category without a positive definition does not get chosen.** `other = "alles andere"` sounds complete but does not work: the model prefers to reach for a category with concrete features. Recall rose from 0.43 to 0.86 after `other` got its own features (press inquiries, job applications, opinions without a call to action, test messages).

**The model follows the rule as written — not the one that was meant.** A ticket saying *"Bin die nächsten 3 Monate im Ausland"* (I'm abroad for the next 3 months) was classified as urgent because the rule read "explizite Zeitangabe oder Frist". That was formally correct and wrong on the substance. Cases like this are not found by thinking about the prompt, but only by looking at the errors one by one.

**A checking tool finds problems that aren't problems — if you forget the cross-check.** The LLM judge reported two gaps in the urgency rules: there was no matching `high` condition for a reported unauthorized access to an account or for a GDPR request with a statutory deadline. Both were true. A v4 was then created that closed both gaps — with the result that category accuracy fell by 5.4 percentage points, urgency accuracy did not move and costs rose by 9%. The reason: the affected tickets had **already been classified correctly** in v3. The judge checks labels against rules, not the classifier against the Goldset — so a rule gap it finds is not automatically a source of errors. A look at `predictions_v3.csv` would have shown this in seconds. v4 was reverted; the run is included as `evals/*_v4_reverted.*`, and since then the rule has been: a judge finding only becomes a prompt change if the classifier is also wrong on the same ticket. Incidentally, the regression test correctly flagged the degradation — that was its first real use.

**Errors in the Goldset get blamed on the classifier.** While setting up the harness, two label errors came to light that a manual review had missed. Had they been left in place, they would have entered the matrix as model errors — with the wrong conclusion that the prompt needed work.

**Documentation drifts faster than you think.** Twice in this project a docstring described a state the code no longer had: once the claim "byte-identisch mit UC1" (byte-identical to UC1) after the prompt had already been changed, once a fixed file path after the artifacts had been switched to tags. Both were only noticed because someone looked on purpose. In a repo whose very purpose is traceability of versions, this is the most dangerous class of error.

## What I Would Do Differently

**Run every version several times.** All numbers here come from a single run per version. The sentiment drop from 86.3% to 84.9% corresponds to one net ticket — whether that is noise or a real effect cannot be told with n=1 runs. Three to five runs per version with a spread figure would be the small extra cost (one run costs about $0.16) that would make all comparisons robust.

**Check the Goldset against the schema definitions before the first run.** The biggest single finding of the baseline — sentiment at 68.5% — turned out in the end not to be a model error but a definition conflict: the schema required explicit anger, while the Goldset labeled every problem report as negative. Both sides were internally consistent and contradicted each other. A comparison up front would have saved an entire measurement cycle.

**Think about the thin classes when drafting the Goldset.** `positive` with n=2 should have stood out while writing the tickets, not only during scoring.

**Check prompt caching earlier.** That the domain logic lives in the schema and is therefore paid for again with every request was foreseeable from the start. The cost curve across three versions (+62%) could have been kept flatter.

---

## Usage

```bash
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-..." > .env

python score.py --tag v3 --workers 1 --out evals/results_v3.md  # run + report
python score.py --tag v3 --from-cache                           # recompute only, free
```

### Regression Test

Checks a run's metrics against fixed thresholds and exits with exit code 1 if one is not met — so it can be hooked into a pre-commit hook or a CI stage.

```bash
python evals/test_regression.py --tag v3          # against existing run, free
python evals/test_regression.py --tag v4 --run    # classify fresh, then check
```

| Metric | Threshold | v3 |
|---|---:|---:|
| Category accuracy | ≥ 85% | 89.0% |
| Urgency accuracy | ≥ 75% | 79.5% |
| Sentiment accuracy | ≥ 80% | 84.9% |

The thresholds are deliberately set below the v3 level. They are meant to catch real regressions, not the spread between two runs of the same prompt — as long as each version is not measured multiple times (see *What I Would Do Differently*), the margin below is the safeguard against false alarms. As a sanity check: against the baseline run, the test fails on all three metrics.

### Goldset Audit (LLM-as-Judge)

A second model (Sonnet, deliberately not the Haiku classifier — a model that grades its own judgment tends toward self-confirmation) checks every label against the rules from `classify.py` and flags contradictions.

```bash
python evals/audit_goldset.py --tag v3               # run, ~$0.68
python evals/audit_goldset.py --tag v3 --from-cache  # only re-render report
```

The judge **never** changes a label. It produces a candidate list for manual review; a human makes the decision. It reads the rules directly from `CLASSIFY_TOOL` — if an enum description changes there, the next run automatically audits against the new version.

| File | Content |
|---|---|
| `evals/goldset.csv` | 73 tickets, hand-labeled |
| `evals/predictions_<tag>.csv` | raw results per run (incl. latency and tokens) |
| `evals/results_<tag>.md` | scoring per run |
| `evals/goldset_audit_<tag>.md` | contradictions from the LLM audit |
| `evals/*_v4_reverted.*` | reverted experiment, see `docs/decisions.md` |
| `docs/decisions.md` | dated decisions, incl. the decoupling from UC1 |
