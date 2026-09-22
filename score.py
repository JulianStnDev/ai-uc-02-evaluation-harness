"""Evaluation-Harness: klassifiziert das Goldset und vergleicht mit den Labels.

Zwei getrennte Phasen, damit die Auswertung nichts kostet:

  1. Lauf    -> ruft classify() fuer jedes Ticket, schreibt evals/predictions.csv
  2. Scoring -> rechnet alle Metriken aus evals/predictions.csv

Mit --from-cache wird Phase 1 uebersprungen. Die Auswertung laesst sich damit
beliebig oft umbauen, ohne erneut die API zu bezahlen.

    python score.py                  # Lauf + Scoring
    python score.py --workers 1      # seriell (ehrliche Latenzmessung)
    python score.py --from-cache     # nur neu rechnen, keine Requests
    python score.py --from-cache --out evals/results.md
"""
import argparse, csv, json, os, statistics, sys, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

GOLDSET = "evals/goldset.csv"
PREDICTIONS = "evals/predictions.csv"
RUN_META = "evals/run_meta.json"

# Reihenfolge wie im Enum in classify.py — bestimmt die Achsen der Konfusionsmatrix.
CATEGORIES = ["billing", "technical", "account", "feature-request", "other"]
SENTIMENTS = ["positive", "neutral", "negative"]
# Ordinal: Abstand zwischen den Stufen ist die Basis fuer Unter-/Ueberschaetzung.
URGENCY = {"low": 0, "medium": 1, "high": 2}
URGENCY_ORDER = ["low", "medium", "high"]

# Haiku 4.5, Stand Sept 2026. Muss mit dem Modell in classify.py zusammenpassen.
PRICE_IN_PER_MTOK = 1.00
PRICE_OUT_PER_MTOK = 5.00


# --------------------------------------------------------------------------
# Phase 1: Lauf
# --------------------------------------------------------------------------

def load_goldset(path=GOLDSET):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    labeled = [r for r in rows if r["category"] and r["urgency"] and r["sentiment"]]
    skipped = len(rows) - len(labeled)
    if skipped:
        print(f"Hinweis: {skipped} Zeile(n) ohne vollstaendige Labels werden uebersprungen.")
    return labeled


def run(tickets, workers):
    """Klassifiziert alle Tickets und schreibt predictions.csv. Gibt die Rows zurueck."""
    from classify import classify  # erst hier, damit --from-cache ohne API-Key laeuft

    def one(t):
        try:
            result, latency, itok, otok = classify(t["text"])
            return {"id": t["id"], "category": result["category"],
                    "urgency": result["urgency"], "sentiment": result["sentiment"],
                    "latency_s": f"{latency:.3f}", "input_tokens": itok,
                    "output_tokens": otok, "error": ""}
        except Exception as e:  # ein kaputtes Ticket darf den Lauf nicht abbrechen
            return {"id": t["id"], "category": "", "urgency": "", "sentiment": "",
                    "latency_s": "", "input_tokens": "", "output_tokens": "",
                    "error": f"{type(e).__name__}: {e}"}

    started = time.time()
    print(f"Klassifiziere {len(tickets)} Tickets mit {workers} Worker(n) ...")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(one, tickets))
    wall = time.time() - started

    fields = ["id", "category", "urgency", "sentiment", "latency_s",
              "input_tokens", "output_tokens", "error"]
    with open(PREDICTIONS, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    meta = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "model": _model_from_classify(), "workers": workers,
            "n": len(rows), "wall_clock_s": round(wall, 1),
            "errors": sum(1 for r in rows if r["error"])}
    with open(RUN_META, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Fertig in {wall:.1f}s -> {PREDICTIONS}")
    return rows


def _model_from_classify():
    """Liest die Model-ID aus classify.py, ohne sie hier zu duplizieren."""
    import re
    src = open("classify.py", encoding="utf-8").read()
    m = re.search(r'model="([^"]+)"', src)
    return m.group(1) if m else "unbekannt"


def load_predictions(path=PREDICTIONS):
    if not os.path.exists(path):
        sys.exit(f"{path} existiert nicht — einmal ohne --from-cache laufen lassen.")
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


# --------------------------------------------------------------------------
# Phase 2: Metriken
# --------------------------------------------------------------------------

def confusion(pairs, labels):
    """pairs = [(gold, pred), ...] -> matrix[gold][pred]"""
    m = {g: Counter() for g in labels}
    for gold, pred in pairs:
        m[gold][pred] += 1
    return m


def render_matrix(m, labels, short):
    """Zeilen = Gold, Spalten = Prediction."""
    w = max(len(s) for s in short) + 2
    head = " " * 18 + "".join(f"{short[l]:>{w}}" for l in labels) + f"{'Summe':>8}"
    lines = ["  (Zeile = Gold, Spalte = Prediction)", "", head]
    for g in labels:
        total = sum(m[g].values())
        cells = "".join(f"{(m[g][p] or '.'):>{w}}" for p in labels)
        lines.append(f"  {g:<16}{cells}{total:>8}")
    col_totals = "".join(f"{sum(m[g][p] for g in labels):>{w}}" for p in labels)
    lines.append(f"  {'Summe':<16}{col_totals}{sum(sum(m[g].values()) for g in labels):>8}")
    return "\n".join(lines)


def per_class(m, labels):
    """Precision/Recall/F1 je Klasse."""
    out = []
    for c in labels:
        tp = m[c][c]
        support = sum(m[c].values())                      # Gold-Zeile
        predicted = sum(m[g][c] for g in labels)          # Prediction-Spalte
        prec = tp / predicted if predicted else 0.0
        rec = tp / support if support else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
        out.append({"label": c, "support": support, "predicted": predicted,
                    "precision": prec, "recall": rec, "f1": f1})
    return out


def percentile(values, q):
    """Nearest-Rank-Perzentil (kein Interpolieren — bei n=73 ehrlicher)."""
    if not values:
        return float("nan")
    s = sorted(values)
    import math
    rank = max(1, math.ceil(q * len(s)))
    return s[rank - 1]


def build_report(gold_rows, pred_rows, meta):
    gold = {r["id"]: r for r in gold_rows}
    ok = [p for p in pred_rows if not p["error"] and p["id"] in gold]
    failed = [p for p in pred_rows if p["error"]]
    L = []
    add = L.append

    n = len(ok)
    add(f"# Evaluationsergebnisse\n")
    add(f"- Goldset: {len(gold_rows)} gelabelte Tickets")
    add(f"- Ausgewertet: {n}" + (f" ({len(failed)} Fehler, siehe unten)" if failed else ""))
    add(f"- Modell: `{meta.get('model', '?')}`")
    add(f"- Lauf: {meta.get('timestamp', '?')}, {meta.get('workers', '?')} Worker\n")

    # ---------------- Category ----------------
    pairs = [(gold[p["id"]]["category"], p["category"]) for p in ok]
    m = confusion(pairs, CATEGORIES)
    acc = sum(1 for g, pr in pairs if g == pr) / n if n else 0.0
    short = {"billing": "bill", "technical": "tech", "account": "acct",
             "feature-request": "feat", "other": "other"}

    add("## Category\n")
    add(f"**Accuracy: {acc:.1%}** ({sum(1 for g, pr in pairs if g == pr)}/{n})\n")
    add("```")
    add(render_matrix(m, CATEGORIES, short))
    add("```\n")

    rows = per_class(m, CATEGORIES)
    add("| Klasse | Support | Precision | Recall | F1 |")
    add("|---|---:|---:|---:|---:|")
    for r in rows:
        add(f"| {r['label']} | {r['support']} | {r['precision']:.2f} | "
            f"{r['recall']:.2f} | {r['f1']:.2f} |")
    macro = sum(r["f1"] for r in rows) / len(rows)
    add(f"\nMacro-F1: **{macro:.3f}**\n")

    confusions = Counter()
    for g, pr in pairs:
        if g != pr:
            confusions[(g, pr)] += 1
    if confusions:
        add("Haeufigste Verwechslungen (Gold -> Prediction):\n")
        for (g, pr), c in confusions.most_common(5):
            ids = [p["id"] for p in ok
                   if gold[p["id"]]["category"] == g and p["category"] == pr]
            add(f"- `{g}` -> `{pr}`: {c}x  (Tickets {', '.join(ids)})")
        add("")

    # ---------------- Urgency ----------------
    add("## Urgency\n")
    u_pairs = [(gold[p["id"]]["urgency"], p["urgency"], p["id"]) for p in ok]
    u_acc = sum(1 for g, pr, _ in u_pairs if g == pr) / n if n else 0.0
    add(f"**Accuracy: {u_acc:.1%}** ({sum(1 for g, pr, _ in u_pairs if g == pr)}/{n})\n")

    by_delta = defaultdict(list)
    for g, pr, tid in u_pairs:
        by_delta[URGENCY[pr] - URGENCY[g]].append(tid)

    under = {d: ids for d, ids in by_delta.items() if d < 0}   # Modell zu niedrig
    over = {d: ids for d, ids in by_delta.items() if d > 0}    # Modell zu hoch
    n_under = sum(len(v) for v in under.values())
    n_over = sum(len(v) for v in over.values())

    add(f"- **Unterschaetzt** (Modell < Gold): {n_under} ({n_under / n:.1%}) "
        f"— verschleppte Tickets, das teure Versagen")
    add(f"- **Ueberschaetzt** (Modell > Gold): {n_over} ({n_over / n:.1%}) "
        f"— unnoetige Eskalation, das laute Versagen\n")

    add("| Abweichung | Anzahl | Tickets |")
    add("|---|---:|---|")
    for d in (-2, -1, 0, 1, 2):
        ids = by_delta.get(d, [])
        if not ids:
            continue
        name = {-2: "2 Stufen zu niedrig", -1: "1 Stufe zu niedrig", 0: "korrekt",
                1: "1 Stufe zu hoch", 2: "2 Stufen zu hoch"}[d]
        shown = ", ".join(ids) if d != 0 else "—"
        add(f"| {name} | {len(ids)} | {shown} |")
    add("")

    um = confusion([(g, pr) for g, pr, _ in u_pairs], URGENCY_ORDER)
    add("```")
    add(render_matrix(um, URGENCY_ORDER, {u: u for u in URGENCY_ORDER}))
    add("```\n")

    # ---------------- Sentiment ----------------
    add("## Sentiment\n")
    s_pairs = [(gold[p["id"]]["sentiment"], p["sentiment"]) for p in ok]
    s_acc = sum(1 for g, pr in s_pairs if g == pr) / n if n else 0.0
    add(f"**Accuracy: {s_acc:.1%}** ({sum(1 for g, pr in s_pairs if g == pr)}/{n})\n")
    sm = confusion(s_pairs, SENTIMENTS)
    add("```")
    add(render_matrix(sm, SENTIMENTS, {s: s for s in SENTIMENTS}))
    add("```\n")
    sup = Counter(g for g, _ in s_pairs)
    thin = [f"{s} (n={sup[s]})" for s in SENTIMENTS if sup[s] < 5]
    if thin:
        add(f"Achtung: duenne Klasse(n) im Goldset — {', '.join(thin)}. "
            f"Einzelne Fehler verschieben die Accuracy hier stark.\n")

    # ---------------- Kosten & Latenz ----------------
    add("## Kosten & Latenz\n")
    lat = [float(p["latency_s"]) for p in ok if p["latency_s"]]
    itok = [int(p["input_tokens"]) for p in ok if p["input_tokens"]]
    otok = [int(p["output_tokens"]) for p in ok if p["output_tokens"]]
    if lat and itok:
        avg_in, avg_out = statistics.mean(itok), statistics.mean(otok)
        cost_1000 = (avg_in / 1e6 * PRICE_IN_PER_MTOK +
                     avg_out / 1e6 * PRICE_OUT_PER_MTOK) * 1000
        add(f"- **Kosten pro 1000 Requests: ${cost_1000:.3f}** "
            f"(Ø {avg_in:.0f} Input- / {avg_out:.0f} Output-Tokens, "
            f"${PRICE_IN_PER_MTOK:.2f}/${PRICE_OUT_PER_MTOK:.2f} pro Mio)")
        add(f"- **p95-Latenz: {percentile(lat, 0.95):.2f}s** "
            f"(Median {statistics.median(lat):.2f}s, Ø {statistics.mean(lat):.2f}s, "
            f"max {max(lat):.2f}s)")
        add(f"- Kosten des Laufs: ${cost_1000 / 1000 * n:.4f}")
        if meta.get("workers", 1) > 1:
            add(f"\n> Latenz mit {meta['workers']} parallelen Workern gemessen — "
                f"fuer die Zahl im README einmal mit `--workers 1` laufen lassen.")
        add("")

    if failed:
        add("## Fehlgeschlagene Requests\n")
        for p in failed:
            add(f"- Ticket {p['id']}: {p['error']}")
        add("")

    return "\n".join(L), {"category_accuracy": acc, "macro_f1": macro,
                          "urgency_accuracy": u_acc, "sentiment_accuracy": s_acc}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from-cache", action="store_true",
                    help="nur auswerten, keine API-Requests")
    ap.add_argument("--workers", type=int, default=8,
                    help="parallele Requests (1 = seriell, fuer die Latenzmessung)")
    ap.add_argument("--limit", type=int,
                    help="nur die ersten N Tickets (Testlauf)")
    ap.add_argument("--out", help="Report zusaetzlich als Markdown hierhin schreiben")
    args = ap.parse_args()

    gold_rows = load_goldset()
    if args.limit:
        gold_rows = gold_rows[:args.limit]

    if args.from_cache:
        pred_rows = load_predictions()
        meta = json.load(open(RUN_META, encoding="utf-8")) if os.path.exists(RUN_META) else {}
    else:
        pred_rows = run(gold_rows, args.workers)
        meta = json.load(open(RUN_META, encoding="utf-8"))

    report, headline = build_report(gold_rows, pred_rows, meta)
    print("\n" + report)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nReport geschrieben: {args.out}")

    print("Kurzfassung: " + "  ".join(f"{k}={v:.3f}" for k, v in headline.items()))


if __name__ == "__main__":
    main()
