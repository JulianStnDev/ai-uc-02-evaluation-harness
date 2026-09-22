"""Regressionstest: prueft die Metriken eines Laufs gegen feste Schwellenwerte.

Exit-Code 0 = alle Schwellen gehalten, 1 = mindestens eine unterschritten.
Damit laesst sich das Skript in einen Pre-Commit-Hook oder eine CI-Stufe haengen.

Standardmaessig wird aus evals/predictions_<tag>.csv gerechnet — kostet nichts
und setzt voraus, dass der Lauf schon existiert. Mit --run wird vorher frisch
klassifiziert (kostet API-Calls).

    python evals/test_regression.py --tag v3            # gegen letzten Lauf pruefen
    python evals/test_regression.py --tag v4 --run      # frisch klassifizieren + pruefen
"""
import argparse, json, os, sys

# score.py liegt im Repo-Root und arbeitet mit relativen Pfaden.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from score import (build_report, load_goldset, load_predictions,  # noqa: E402
                   meta_path, pred_path, run)

# Abgeleitet vom v3-Stand (89.0 / 79.5 / 84.9) mit Abstand nach unten: die
# Schwellen sollen echte Verschlechterungen fangen, nicht die Streuung zwischen
# zwei Laeufen desselben Prompts.
THRESHOLDS = {
    "category_accuracy": 0.85,
    "urgency_accuracy": 0.75,
    "sentiment_accuracy": 0.80,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tag", default="v3", help="welcher Lauf geprueft wird")
    ap.add_argument("--run", action="store_true",
                    help="vorher frisch klassifizieren (kostet API-Calls)")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    gold = load_goldset()
    if args.run:
        pred = run(gold, args.workers, args.tag)
    else:
        pred = load_predictions(pred_path(args.tag))
    mp = meta_path(args.tag)
    meta = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {}

    _, headline = build_report(gold, pred, meta)

    print(f"Regressionstest gegen Lauf '{args.tag}' (n={len(gold)})\n")
    print(f"  {'Metrik':<22}{'Ist':>8}{'Schwelle':>11}   Status")
    failed = []
    for metric, threshold in THRESHOLDS.items():
        value = headline[metric]
        ok = value >= threshold
        if not ok:
            failed.append((metric, value, threshold))
        print(f"  {metric:<22}{value:>7.1%}{threshold:>11.0%}   {'OK' if ok else 'FEHLGESCHLAGEN'}")

    if failed:
        print(f"\n{len(failed)} Schwelle(n) unterschritten:")
        for metric, value, threshold in failed:
            print(f"  - {metric}: {value:.1%} < {threshold:.0%} "
                  f"(fehlen {(threshold - value) * 100:.1f} Prozentpunkte)")
        return 1

    print("\nAlle Schwellen gehalten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
