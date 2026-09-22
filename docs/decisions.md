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
