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

## 2026-09-22: Bedingung (2) gilt auf Gesamtnutzerbasis, nicht pro Nutzergruppe
Kontext: Im Goldset-Audit schlugen Judge (Sonnet) und Klassifikator (Haiku) unabhängig voneinander
für #44 (VoiceOver-Nutzerin, Timer-Buttons ohne Labels) technical/high statt feature-request/low vor.
Das Argument: Für eine blinde Nutzerin ist der Fokus-Timer durch die fehlenden Labels faktisch
unbedienbar — also ein kompletter Ausfall einer Kernfunktion im Sinne von Bedingung (2).
Entscheidung: #44 bleibt feature-request/low. Bedingung (2) wird auf Gesamtnutzerbasis ausgelegt:
Eine Kernfunktion ist "komplett unbenutzbar", wenn sie für die Nutzerschaft insgesamt ausfällt,
nicht wenn sie für eine einzelne Nutzergruppe unbrauchbar ist.
Begründung: Die Gegenauslegung skaliert nicht. Jede gruppenspezifische Einschränkung — Tablet-Layout,
alte Android-Version, kleiner Bildschirm, langsame Verbindung — wäre für die betroffene Gruppe ein
Totalausfall und damit high. Die Regel würde beliebig weit und verlöre ihre Trennschärfe, genau der
Über-Trigger-Fehler, den die Präzisierung von Bedingung (1) in v3 gerade behoben hat.
Offen und bewusst nicht mitentschieden: ob Accessibility-Tickets eine eigene Behandlung brauchen.
Das ist eine Produktfrage, keine Frage der Dringlichkeitsskala.

## 2026-09-22: v4 zurückgenommen — Judge-Funde sind kein Änderungsgrund für sich
Hypothese: Das Goldset-Audit (Sonnet als Judge) hatte zwei Regellücken in urgency angezeigt — für
#14 (unbefugter Login aus Vietnam) und #21 (DSGVO-Löschung mit gesetzlicher Frist) gab es keine
passende high-Bedingung. v4 ergänzte daher Bedingung (4) für Sicherheits-/Datenschutzvorfälle und
nannte "gesetzliche Frist" ausdrücklich als Beispiel in Bedingung (1).
Ergebnis: Category-Accuracy 89.0% -> 83.6% (4 Tickets gekippt, 0 repariert, obwohl die
Category-Beschreibung unverändert blieb — Kopplungseffekt), Urgency ±0 (79.5%, 4 repariert / 4 neu
falsch), Sentiment ±0 (84.9%), Kosten +$0.21 pro 1000 Requests. Im Judge-Bild wirkte die Änderung
(Urgency-Flags 16 -> 12), in der Messung gegen das Goldset nicht. Entscheidend: #14, #21, #27 und
#64 waren in v3 bereits korrekt als high klassifiziert. Es wurde kein einziger Klassifikator-Fehler
behoben.
Entscheidung: Revert. classify.py steht wieder auf v3, die Schwellen des Regressionstests bleiben
bei 85/75/80 (auf v3 kalibriert — der Test hat die Verschlechterung korrekt gemeldet). Die
v4-Artefakte bleiben als evals/*_v4_reverted.* erhalten.
Begründung / generelle Regel ab jetzt: Ein Judge-Fund wird nur dann zur Prompt-Änderung, wenn der
Klassifikator auf demselben Ticket ebenfalls falsch liegt (Gegenprobe in predictions_<tag>.csv).
Der Judge prüft Label gegen Regeln, nicht Klassifikator gegen Goldset — eine Regellücke, die er
findet, ist nicht automatisch eine Fehlerquelle. Sie zu schließen kostet aber in jedem Fall
Schema-Länge, und über den Kopplungseffekt kippt das an anderer Stelle Labels.

## 2026-09-24: Use Case abgeschlossen

Kontext: Der letzte inhaltliche Stand (v3, v4 zurückgenommen, verbleibende
Widersprüche als bekannte Grenze dokumentiert) ist vom 22.09.2026. Es ist
nichts mehr offen.

Entscheidung: meta.json auf `done`. Die README ist vollständig, einschließlich
der drei Pflichtzahlen (Latenz bewusst als Median, Begründung in der README).
