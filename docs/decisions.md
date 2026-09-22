# Entscheidungen

<!-- Format:
## YYYY-MM-DD: Kurztitel
Kontext, Optionen, Entscheidung, Begründung
-->

## 2026-09-18: Status-Vokabular für meta.json

Kontext: meta.json legt "status": "planned" fest, ohne definierte erlaubte Werte —
das driftet über mehrere Repos auseinander (planned/in-progress/wip/...).

Optionen: (a) einfach: planned → active → done, (b) zusätzlich mit
parked/abandoned für verworfene Use Cases, (c) feiner: research →
building → evaluating → shipped.

Entscheidung: (a) — planned, active, done. Zusätzlich in CLAUDE.md verankert.

Begründung: Bei einem Solo-Portfolio mit meist einem aktiven Repo lohnt sich
keine feinere Staffelung. CLAUDE.md-Verankerung, damit der Agent das Vokabular
bei jedem neuen Repo automatisch mitliest statt dass ich mich erinnern muss.

## 2026-09-22: Tie-Break-Regel für Tickets mit mehreren Themen

Kontext: Einige generierte Test-Tickets sprechen zwei Probleme gleichzeitig an
(z.B. #61: Upsell-Hinweis trotz Pro-Abo + fehlende Gutschrift; #67: ignorierte
Kündigung + trotzdem abgebucht). category ist aber ein Einzelwert.

Entscheidung: category = das schwerwiegendere Thema, nach Rangfolge Geld/Sicherheit
> kompletter Funktionsausfall > Ärgernis/Kosmetik. Das Zweitthema wird in einer
neuen Spalte "notes" festgehalten, nicht ignoriert.

Begründung: Eine "multi"-Kategorie würde die spätere Confusion Matrix unlesbar
machen. Eine reine "zuerst genannt"-Regel wäre willkürlich (hängt nur von
Schreibgewohnheit ab), Schweregrad ist eine inhaltliche Regel.

## 2026-09-22: Zwei Korrekturen aus Claude Codes Code-Review des Goldsets
Kontext: Beim Aufsetzen von score.py wurden zwei weitere Probleme im Goldset gefunden (nicht in der
manuellen Review erkannt).
- #19 ("unsubscribe"): war als technical gelabelt, enthält aber kein technisches Signal. Korrigiert zu
  other, aus demselben Grund wie #9 (kein hinreichendes Signal für eine der vier Kernkategorien).
- #61: notes widersprachen dem Ticket-Inhalt (nannten "account", obwohl das Ticket nur billing +
  technical behandelt). Notes korrigiert zu "multi, billing und technical".
Ergänzend geprüft: #67 (Zweitthema "ignorierte Kündigungs-Einstellung") bleibt technical, nicht
account – Einstellung wurde vom System nicht korrekt verarbeitet, kein Datenproblem im Konto selbst.
Begründung: Bestätigt nochmal den Grundsatz, dass Datenfehler im Goldset dem Klassifikator sonst
fälschlich angelastet würden.

## 2026-09-22: classify.py entkoppelt sich von UC1 (v2)
Kontext: Baseline-Lauf (n=73, $0.10, 82.2% Category-Accuracy) deckte drei Kalibrierungslücken auf,
die mit n=6 in UC1 nicht sichtbar waren: other-Recall 0.43 (Kategorie ohne positive Definition),
Urgency-Überschätzung durch zu breite Zeitbezug-Regel (#49), Sentiment-Definition im Code veraltet
gegenüber der später präzisierten Risiko-Definition.
Entscheidung: classify.py wird für UC2 gezielt an drei Stellen angepasst (category/other,
urgency/Bedingung 1, sentiment/negative). UC1s Repo und README bleiben unverändert als historischer
Stand (n=6, erster Wurf). UC2 führt die Kalibrierung mit n=73 fort.
Begründung: "Byte-identisch" war nötig, um die Baseline fair zu messen — nicht, um den Prompt für
immer einzufrieren. Der Vergleich Baseline vs. korrigierter Lauf ist der eigentliche UC2-Nachweis.
