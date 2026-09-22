# UC2 — Evaluation Harness für Ticket-Klassifikation

## Problem

In [UC1](https://github.com/JulianStnDev/ai-uc-01-ticket-classification) ist ein Klassifikator entstanden, der Support-Tickets nach `category`, `urgency` und `sentiment` einsortiert. Geprüft wurde er gegen 6 Beispiel-Tickets. Bei n=6 lässt sich aber nicht unterscheiden, ob der Prompt wirklich funktioniert oder ob die sechs Beispiele zufällig gepasst haben — und schon gar nicht, ob eine Prompt-Änderung eine Verbesserung ist oder nur die Fehler verschiebt.

Dieses Repo baut den Messaufbau dafür: ein Goldset aus 73 handgelabelten Support-Tickets einer fiktiven Produktivitäts-App (FocusFlow) und ein Harness, das jeden Prompt-Stand dagegen misst — mit Konfusionsmatrix, Fehlerrichtung und Kosten pro Lauf.

Adressat ist die Person, die entscheiden muss, ob ein geänderter Prompt in Produktion darf.

## PM-Entscheidung

**Accuracy allein reicht nicht.** Bei `urgency` sind die beiden Fehlerrichtungen unterschiedlich teuer: Ein unterschätztes Ticket bleibt liegen, ein überschätztes erzeugt eine unnötige Eskalation. Eine gemeinsame Trefferquote versteckt genau diesen Unterschied. Der Harness weist deshalb Unter- und Überschätzung getrennt aus, mit Ticket-IDs, und `category` als vollständige 5×5-Matrix statt als einzelne Prozentzahl.

**Lauf und Auswertung sind getrennt.** `score.py` schreibt erst alle Rohergebnisse nach `evals/predictions_<tag>.csv` und rechnet die Metriken anschließend aus dieser Datei. Mit `--from-cache` lässt sich die Auswertung beliebig oft umbauen, ohne erneut die API zu bezahlen. Jeder Lauf trägt einen Tag, damit ältere Messungen erhalten bleiben und vergleichbar sind.

**Das Goldset ist von Hand gelabelt**, nicht von einem Modell. Ein modellgelabeltes Goldset misst die Übereinstimmung zweier Modelle, nicht die Qualität gegen die fachliche Absicht.

**Der Klassifikator startete byte-identisch zu UC1.** Erst nachdem die Baseline gemessen war, wurde der Prompt gezielt verändert — mit dem ausdrücklichen Vermerk, dass UC1 damit nicht mehr denselben Stand hat. Die Begründung steht in [docs/decisions.md](docs/decisions.md).

## Architekturskizze

```
  evals/goldset.csv                    classify.py
  73 Tickets, 3 Labels                 1 Messages-Call pro Ticket
         │                             tool_choice erzwingt classify_ticket
         │                             3 Enum-Felder, Haiku 4.5
         │                                     │
         └──────────────┬──────────────────────┘
                        ▼
                    score.py
         ┌──────────────┴──────────────┐
    Phase 1: Lauf              Phase 2: Scoring
    ThreadPool, --workers N    liest predictions_<tag>.csv
         │                             │
         ▼                             ▼
  predictions_<tag>.csv        Konfusionsmatrix, P/R/F1,
  run_meta_<tag>.json          Fehlerrichtung, Kosten, Latenz
                                       │
                                       ▼
                               results_<tag>.md
```

Kein Framework, direkt gegen das Anthropic SDK. Die Klassifikation nutzt erzwungenen Tool-Use (`tool_choice`), damit die Antwort schema-valide zurückkommt und kein Parsing nötig ist. Die gesamte Fachlogik steckt in den `description`-Feldern der drei Enums — das ist die Stellschraube, an der die drei Versionen unten sich unterscheiden.

## Evaluationsergebnisse

n=73, seriell gemessen (`--workers 1`), Modell `claude-haiku-4-5`, ein Lauf je Version.

| Metrik | Baseline (= UC1) | v2 | v3 |
|---|---:|---:|---:|
| **Category-Accuracy** | 82.2% | 86.3% | **89.0%** |
| Macro-F1 | 0.801 | 0.858 | **0.889** |
| **Urgency-Accuracy** | 71.2% | 68.5% | **79.5%** |
| — unterschätzt (Ticket bleibt liegen) | 7 | 14 | **8** |
| — überschätzt (unnötige Eskalation) | 14 | 9 | **7** |
| **Sentiment-Accuracy** | 68.5% | **86.3%** | 84.9% |
| Kosten / 1000 Requests | $1.38 | $1.86 | $2.23 |
| Median-Latenz | 0.87s | 0.90s | 0.92s |

### Wie es dazu kam

**Die Baseline legte drei Kalibrierungslücken offen**, die bei n=6 unsichtbar geblieben waren. Die auffälligste: `other` hatte einen Recall von 0.43 — die Kategorie war als „alles andere" beschrieben, während die vier übrigen konkrete Bedingungen nannten. Eine Kategorie ohne positives Merkmal verliert jeden Zweikampf gegen eine mit. Dazu kam eine zu weit gefasste Dringlichkeitsregel („explizite Zeitangabe **oder** Frist"), die jeden Zeitbezug im Text als Frist las, und eine Sentiment-Definition, die nur auf wütenden Tonfall ansprang und sachlich formulierte Schadensmeldungen als neutral einstufte.

**v2 korrigierte alle drei** — und brachte Sentiment von 68.5% auf 86.3%, ohne ein einziges Ticket zu verschlechtern. Gleichzeitig **fiel Urgency auf 68.5%**. Die Ursache war aufschlussreich: Die präzisierte Fristregel entfernte eine Stütze, auf der Tickets bis dahin unbemerkt gelaufen waren. Vier Tickets, die die Baseline korrekt als `high` erkannt hatte, waren nie über die Bedingung „Kernfunktion unbenutzbar" eingestuft worden, sondern über den lockeren Zeitbezug. Am deutlichsten bei einem Ticket, in dem die App direkt beim Start abstürzt — Lehrbuchfall für „Kernfunktion unbenutzbar", und die Regel griff trotzdem nicht. Zusätzlich zeigte sich, dass für eingetretenen Geldverlust **überhaupt keine Regel existierte**: Das Goldset stufte solche Tickets als `high` ein, die Enum-Beschreibung kannte diesen Fall nicht.

**v3 setzte genau dort an**: konkrete Beispiele für „Kernfunktion unbenutzbar" und eine neue, bewusst eng gefasste Bedingung für bereits eingetretenen, bezifferten Geldschaden. Ergebnis: 9 Tickets repariert, 1 neu falsch — und die Überschätzung kam **nicht** zurück, sondern fiel mit 7 Fällen auf den niedrigsten Wert aller drei Läufe.

### Bekannte Grenzen

**Vier `high`-Tickets werden weiterhin unterschätzt.** Bei zweien ist das der bewusst gewählte Preis der engen Fassung: Sie beschreiben eingetretenen Geldschaden, nennen aber keinen Betrag, und die Regel verlangt eine Bezifferung. Würde man das lockern, käme mit hoher Wahrscheinlichkeit die Über-Eskalation zurück, die v3 gerade beseitigt hat. Ein drittes Ticket (*„passwort funktioniert nicht mehr"*) fällt wörtlich unter „Login dauerhaft nicht möglich" und wird trotzdem `medium` — dafür gibt es bisher keine Erklärung.

**Zwei `billing`/`other`-Grenzfälle bleiben offen.** Die Abgrenzungsregel („konkrete Transaktion im eigenen Vertrag" vs. „allgemeine Kritik am Preisniveau") ordnet eine Beschwerde über eine Preiserhöhung eindeutig `billing` zu — das Modell wählt trotzdem `other`. Eine Anfrage nach Bildungsrabatten wandert aus demselben Grund in die falsche Richtung. Diese beiden Tickets sind die gesamte verbleibende `billing`-Schwäche (Recall 0.85).

**Eine Sentiment-Klasse ist zu dünn.** `positive` kommt im Goldset nur zweimal vor. Die Sentiment-Accuracy sagt über diese Klasse praktisch nichts aus; `score.py` warnt inzwischen automatisch bei Klassen unter n=5.

## Kosten & Latenz

- **Kosten pro 1000 Requests: $2.23** (Ø 1886 Input- / 68 Output-Tokens, Haiku 4.5 zu $1/$5 pro Mio Tokens)
- **Median-Latenz: 0.92s** ¹
- **Qualitätsmetrik: 89.0% Category-Accuracy** (Macro-F1 0.889)

¹ Bewusst der Median statt p95. Bei n=73 sitzt das 95. Perzentil auf Rang 70, ein einzelner Ausreißer schlägt also voll durch — im v3-Lauf brauchte ein Request 7.03s und hob p95 auf 1.90s, während der Median unverändert bei 0.92s lag. Eine p95-Zahl wäre bei dieser Stichprobengröße eine Scheingenauigkeit.

### Kosten gegen Qualität

Die gesamte Fachlogik steckt in den Enum-Beschreibungen, und die werden bei jedem Request neu übertragen. Das Schema wuchs über die drei Versionen von 1180 auf 3344 Zeichen, die Input-Tokens von 1036 auf 1886 — bei einem durchschnittlichen Ticket von wenigen Dutzend Tokens macht das Schema damit den weit überwiegenden Teil der Kosten aus.

| | Baseline → v3 |
|---|---|
| Kosten | **+62%** |
| Category-Accuracy | +6.8pp |
| Urgency-Accuracy | +8.3pp |
| Sentiment-Accuracy | +16.4pp |

Ob dieser Tausch sich lohnt, hängt am Anwendungsfall: Bei 100.000 Tickets im Monat sind das $223 statt $138. Ein ungeprüfter Hebel ist Prompt Caching — es würde genau den Schema-Anteil treffen, setzt aber eine Mindestlänge des gecachten Prefix voraus, die noch nicht verifiziert wurde.

## Learnings

**Drei Felder in einem Tool-Call sind nicht unabhängig voneinander.** In v3 wurde ausschließlich an `category` und `urgency` geändert — die Sentiment-Accuracy fiel trotzdem um 1,4pp (3 Tickets repariert, 4 neu falsch). Alle drei Werte entstehen in derselben Antwort; eine Änderung an einer Beschreibung kann die Ausgabe der anderen mitverschieben. Praktische Folge: Man kann die drei Metriken nicht getrennt optimieren, und ein einzelner Lauf reicht nicht, um 1–2pp von Streuung zu unterscheiden.

**Eine Kategorie ohne positive Definition wird nicht gewählt.** `other = "alles andere"` klingt vollständig, funktioniert aber nicht: Das Modell greift lieber nach einer Kategorie mit konkreten Merkmalen. Recall stieg von 0.43 auf 0.86, nachdem `other` eigene Merkmale bekam (Presseanfragen, Bewerbungen, Meinungsäußerungen ohne Handlungsaufforderung, Testnachrichten).

**Das Modell befolgt die Regel, die dasteht — nicht die, die gemeint war.** Ein Ticket mit *„Bin die nächsten 3 Monate im Ausland"* wurde als dringend eingestuft, weil die Regel „explizite Zeitangabe oder Frist" lautete. Das war formal korrekt und fachlich falsch. Solche Fälle findet man nicht durch Nachdenken über den Prompt, sondern nur, indem man die Fehler einzeln anschaut.

**Ein Prüfwerkzeug findet Probleme, die keine sind — wenn man die Gegenprobe vergisst.** Der LLM-Judge meldete zwei Lücken in den Dringlichkeitsregeln: Für einen gemeldeten Fremdzugriff aufs Konto und für eine DSGVO-Anfrage mit gesetzlicher Frist gab es keine passende `high`-Bedingung. Beides stimmte. Daraufhin entstand eine v4, die beide Lücken schloss — mit dem Ergebnis, dass die Category-Accuracy um 5,4 Prozentpunkte fiel, die Urgency-Accuracy sich nicht bewegte und die Kosten um 9% stiegen. Der Grund: Die betroffenen Tickets waren in v3 **bereits korrekt** klassifiziert. Der Judge prüft Label gegen Regeln, nicht Klassifikator gegen Goldset — eine Regellücke, die er findet, ist deshalb nicht automatisch eine Fehlerquelle. Ein Blick in `predictions_v3.csv` hätte das in Sekunden gezeigt. v4 wurde zurückgenommen; der Lauf liegt als `evals/*_v4_reverted.*` bei, und seitdem gilt die Regel: Ein Judge-Fund wird nur dann zur Prompt-Änderung, wenn der Klassifikator auf demselben Ticket ebenfalls falsch liegt. Der Regressionstest hat die Verschlechterung übrigens korrekt gemeldet — das war sein erster echter Einsatz.

**Fehler im Goldset werden dem Klassifikator angelastet.** Beim Aufsetzen des Harness fielen zwei Label-Fehler auf, die eine manuelle Durchsicht übersehen hatte. Hätte man sie stehen lassen, wären sie als Modellfehler in die Matrix eingegangen — mit der falschen Schlussfolgerung, am Prompt arbeiten zu müssen.

**Dokumentation driftet schneller, als man denkt.** Zweimal in diesem Projekt beschrieb ein Docstring einen Zustand, den der Code nicht mehr hatte: einmal die Behauptung „byte-identisch mit UC1", nachdem der Prompt bereits geändert war, einmal ein fester Dateipfad, nachdem die Artefakte auf Tags umgestellt worden waren. Beides fiel nur auf, weil jemand gezielt hinsah. In einem Repo, dessen Zweck gerade die Nachvollziehbarkeit von Ständen ist, ist das die gefährlichste Fehlerklasse.

## Was ich anders machen würde

**Jede Version mehrfach laufen lassen.** Alle Zahlen hier stammen aus einem einzigen Lauf je Version. Der Sentiment-Rückgang von 86.3% auf 84.9% entspricht einem Netto-Ticket — ob das Rauschen ist oder ein echter Effekt, lässt sich mit n=1 Läufen nicht sagen. Drei bis fünf Läufe je Version mit Streuungsangabe wären der geringe Aufpreis (ein Lauf kostet rund $0.16), der alle Vergleiche belastbar machen würde.

**Das Goldset vor dem ersten Lauf gegen die Schema-Definitionen prüfen.** Der größte Einzelbefund der Baseline — Sentiment bei 68.5% — war am Ende kein Modellfehler, sondern ein Definitionskonflikt: Das Schema verlangte expliziten Ärger, das Goldset labelte jede Problemmeldung als negativ. Beide Seiten waren in sich schlüssig und widersprachen einander. Ein Abgleich vorab hätte einen ganzen Messzyklus gespart.

**Die dünnen Klassen beim Goldset-Entwurf mitdenken.** `positive` mit n=2 hätte beim Schreiben der Tickets auffallen müssen, nicht erst beim Auswerten.

**Prompt Caching früher prüfen.** Dass die Fachlogik im Schema steckt und damit bei jedem Request neu bezahlt wird, war von Anfang an absehbar. Die Kostenkurve über drei Versionen (+62%) hätte man flacher halten können.

---

## Benutzung

```bash
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-..." > .env

python score.py --tag v3 --workers 1 --out evals/results_v3.md  # Lauf + Report
python score.py --tag v3 --from-cache                           # nur neu rechnen, kostenlos
```

### Regressionstest

Prüft die Metriken eines Laufs gegen feste Schwellen und endet mit Exit-Code 1, wenn eine unterschritten wird — damit lässt er sich in einen Pre-Commit-Hook oder eine CI-Stufe hängen.

```bash
python evals/test_regression.py --tag v3          # gegen bestehenden Lauf, kostenlos
python evals/test_regression.py --tag v4 --run    # frisch klassifizieren, dann prüfen
```

| Metrik | Schwelle | v3 |
|---|---:|---:|
| Category-Accuracy | ≥ 85% | 89.0% |
| Urgency-Accuracy | ≥ 75% | 79.5% |
| Sentiment-Accuracy | ≥ 80% | 84.9% |

Die Schwellen liegen bewusst unter dem v3-Stand. Sie sollen echte Verschlechterungen fangen, nicht die Streuung zwischen zwei Läufen desselben Prompts — solange nicht mehrfach pro Version gemessen wird (siehe *Was ich anders machen würde*), ist der Abstand nach unten die Absicherung gegen Fehlalarme. Zur Kontrolle: Gegen den Baseline-Lauf schlägt der Test in allen drei Metriken fehl.

### Goldset-Audit (LLM-as-Judge)

Ein zweites Modell (Sonnet, bewusst nicht der Haiku-Klassifikator — ein Modell, das sein eigenes Urteil bewertet, neigt zur Selbstbestätigung) prüft jedes Label gegen die Regeln aus `classify.py` und markiert Widersprüche.

```bash
python evals/audit_goldset.py --tag v3               # Lauf, ~$0.68
python evals/audit_goldset.py --tag v3 --from-cache  # nur Report neu rendern
```

Der Judge ändert **nie** ein Label. Er erzeugt eine Kandidatenliste für die manuelle Nachprüfung; die Entscheidung trifft ein Mensch. Die Regeln liest er direkt aus `CLASSIFY_TOOL` — ändert sich dort eine Enum-Beschreibung, auditiert der nächste Lauf automatisch gegen die neue Fassung.

| Datei | Inhalt |
|---|---|
| `evals/goldset.csv` | 73 Tickets, handgelabelt |
| `evals/predictions_<tag>.csv` | Rohergebnisse je Lauf (inkl. Latenz und Tokens) |
| `evals/results_<tag>.md` | Auswertung je Lauf |
| `evals/goldset_audit_<tag>.md` | Widersprüche aus dem LLM-Audit |
| `evals/*_v4_reverted.*` | zurückgenommenes Experiment, siehe `docs/decisions.md` |
| `docs/decisions.md` | datierte Entscheidungen, inkl. der Entkopplung von UC1 |
