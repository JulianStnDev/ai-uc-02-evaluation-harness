"""LLM-as-Judge als Goldset-Auditor.

Prueft NICHT den Klassifikator — das macht score.py. Dieses Skript prueft das
Goldset selbst: Stimmt das von Hand vergebene Label mit den Regeln ueberein,
nach denen klassifiziert werden soll?

Aufbau:
  - Judge ist Sonnet, der Klassifikator ist Haiku. Bewusst ein anderes Modell:
    ein Modell, das sein eigenes Urteil bewertet, neigt zur Selbstbestaetigung.
  - Die Regeln kommen unveraendert aus classify.py (CLASSIFY_TOOL), nicht als
    Kopie. Aendert sich dort eine Enum-Beschreibung, auditiert dieses Skript
    automatisch gegen die neue Fassung.
  - Der Judge aendert NIE ein Label. Er markiert Kandidaten fuer die manuelle
    Nachpruefung. Jede Entscheidung darueber trifft ein Mensch.

    python evals/audit_goldset.py              # Lauf + Report (kostet API-Calls)
    python evals/audit_goldset.py --from-cache # nur Report neu rendern
"""
import argparse, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor

# score.py und classify.py liegen im Repo-Root und arbeiten mit relativen Pfaden.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

import csv  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from anthropic import Anthropic  # noqa: E402
from classify import CLASSIFY_TOOL  # noqa: E402

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Anderes Modell als der Klassifikator (Haiku) — siehe Modul-Docstring.
JUDGE_MODEL = "claude-sonnet-5"
GOLDSET = "evals/goldset.csv"
RAW = "evals/goldset_audit_raw.json"
REPORT = "evals/goldset_audit.md"

FIELDS = ["category", "urgency", "sentiment"]

AUDIT_TOOL = {
    "name": "audit_label",
    "description": "Prueft ein vergebenes Label gegen die Klassifikationsregeln",
    "input_schema": {
        "type": "object",
        "properties": {
            f"{f}_agrees": {
                "type": "boolean",
                "description": f"true, wenn das vergebene {f}-Label nach den Regeln vertretbar ist",
            }
            for f in FIELDS
        } | {
            f"{f}_suggested": {
                "type": "string",
                "enum": CLASSIFY_TOOL["input_schema"]["properties"][f]["enum"],
                "description": f"Bei Zustimmung das bestehende {f}-Label wiederholen, "
                               f"sonst der Wert, den die Regeln verlangen",
            }
            for f in FIELDS
        } | {
            f"{f}_reason": {
                "type": "string",
                "description": f"Nur bei Nichtzustimmung: in einem Satz, welche Regel dagegen "
                               f"spricht. Bei Zustimmung ein leerer String.",
            }
            for f in FIELDS
        },
        "required": [f"{f}_{s}" for f in FIELDS for s in ("agrees", "suggested", "reason")],
    },
}


def rules_text():
    """Die Enum-Beschreibungen aus classify.py, woertlich."""
    props = CLASSIFY_TOOL["input_schema"]["properties"]
    return "\n\n".join(f"{f.upper()} (erlaubt: {', '.join(props[f]['enum'])})\n{props[f]['description']}"
                       for f in FIELDS)


PROMPT = """Du pruefst die Qualitaet eines Goldsets fuer eine Ticket-Klassifikation.

Ein Mensch hat das folgende Support-Ticket von Hand gelabelt. Deine Aufgabe ist
NICHT, selbst frei zu klassifizieren, sondern zu pruefen, ob das vergebene Label
nach den unten stehenden Regeln vertretbar ist.

Wichtig: Bei mehrdeutigen Tickets gibt es oft mehr als eine vertretbare Antwort.
Stimme dem Label zu, solange es sich mit den Regeln begruenden laesst — auch wenn
du selbst anders entschieden haettest. Widersprich nur, wenn das Label einer Regel
klar zuwiderlaeuft.

REGELN
{rules}

TICKET
{text}

VERGEBENES LABEL
category: {category}
urgency: {urgency}
sentiment: {sentiment}

Pruefe jedes der drei Felder einzeln."""


def audit_one(row):
    msg = PROMPT.format(rules=rules_text(), text=row["text"], category=row["category"],
                        urgency=row["urgency"], sentiment=row["sentiment"])
    response = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=1000,
        thinking={"type": "disabled"},  # erzwungener Tool-Use + deterministische Kosten
        tools=[AUDIT_TOOL],
        tool_choice={"type": "tool", "name": "audit_label"},
        messages=[{"role": "user", "content": msg}],
    )
    verdict = next(b for b in response.content if b.type == "tool_use").input
    return {"id": row["id"], "verdict": verdict,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens}


def run(rows, workers):
    def one(r):
        try:
            return audit_one(r)
        except Exception as e:
            return {"id": r["id"], "verdict": None, "error": f"{type(e).__name__}: {e}"}

    started = time.time()
    print(f"Auditiere {len(rows)} Tickets mit {JUDGE_MODEL} ({workers} Worker) ...")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(one, rows))
    payload = {"model": JUDGE_MODEL, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
               "n": len(results), "results": results}
    with open(RAW, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Fertig in {time.time() - started:.1f}s -> {RAW}")
    return payload


def build_report(gold, payload):
    by_id = {r["id"]: r for r in payload["results"]}
    failed = [r for r in payload["results"] if r.get("error")]

    flagged = []   # (id, feld, gold_wert, judge_wert, begruendung)
    for row in gold:
        res = by_id.get(row["id"])
        if not res or not res.get("verdict"):
            continue
        v = res["verdict"]
        for f in FIELDS:
            if not v[f"{f}_agrees"]:
                flagged.append((row["id"], f, row[f], v[f"{f}_suggested"],
                                v[f"{f}_reason"].strip()))

    n = len([r for r in payload["results"] if r.get("verdict")])
    checks = n * len(FIELDS)
    L = [f"# Goldset-Audit\n",
         f"- Judge: `{payload['model']}` (Klassifikator ist Haiku — bewusst ein anderes",
         f"  Modell, damit kein Self-Preference-Bias das Urteil faerbt)",
         f"- Geprueft: {n} Tickets x {len(FIELDS)} Felder = {checks} Einzelurteile",
         f"- Lauf: {payload['timestamp']}",
         f"- **Widersprueche: {len(flagged)}** ({len(flagged) / checks:.1%} der Einzelurteile)\n",
         "> Der Judge aendert keine Labels. Jeder Eintrag unten ist ein Kandidat fuer",
         "> manuelle Nachpruefung — die Entscheidung trifft ein Mensch.\n"]

    if not flagged:
        L.append("Keine Widersprueche gefunden.\n")
    else:
        per_field = {f: sum(1 for x in flagged if x[1] == f) for f in FIELDS}
        L.append("| Feld | Widersprueche |")
        L.append("|---|---:|")
        for f in FIELDS:
            L.append(f"| {f} | {per_field[f]} |")
        L.append("")
        gold_by_id = {r["id"]: r for r in gold}
        for f in FIELDS:
            rows = [x for x in flagged if x[1] == f]
            if not rows:
                continue
            L.append(f"## {f} ({len(rows)})\n")
            for tid, _, gold_val, judge_val, reason in sorted(rows, key=lambda x: int(x[0])):
                text = gold_by_id[tid]["text"]
                L.append(f"**#{tid}** — Goldset `{gold_val}` / Judge `{judge_val}`  ")
                L.append(f"> {text[:200]}{'...' if len(text) > 200 else ''}\n")
                L.append(f"{reason}\n")

    if failed:
        L.append("## Fehlgeschlagene Requests\n")
        L += [f"- Ticket {r['id']}: {r['error']}" for r in failed]
        L.append("")

    itok = sum(r.get("input_tokens", 0) for r in payload["results"])
    otok = sum(r.get("output_tokens", 0) for r in payload["results"])
    # Sonnet 5: $2 / $10 pro Mio Tokens, Stand Sept 2026.
    cost = itok / 1e6 * 2.00 + otok / 1e6 * 10.00
    L.append(f"---\n\nKosten des Audit-Laufs: ${cost:.4f} ({itok} Input- / {otok} Output-Tokens)")
    return "\n".join(L), flagged


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from-cache", action="store_true", help="nur Report neu rendern")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    with open(GOLDSET, encoding="utf-8") as f:
        gold = [r for r in csv.DictReader(f) if r["category"]]

    if args.from_cache:
        if not os.path.exists(RAW):
            sys.exit(f"{RAW} existiert nicht — einmal ohne --from-cache laufen lassen.")
        payload = json.load(open(RAW, encoding="utf-8"))
    else:
        payload = run(gold, args.workers)

    report, flagged = build_report(gold, payload)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n{REPORT} geschrieben — {len(flagged)} Widerspruch/Widersprueche.")


if __name__ == "__main__":
    main()
