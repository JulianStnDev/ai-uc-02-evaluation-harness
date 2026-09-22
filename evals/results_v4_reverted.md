# Evaluationsergebnisse

> **Zurueckgenommenes Experiment.** Die Prompt-Aenderung, die diesen Lauf erzeugt hat,
> wurde verworfen; classify.py steht wieder auf v3. Der Lauf bleibt als Beleg stehen.
> Begruendung: docs/decisions.md, Eintrag "v4 zurueckgenommen".


- Goldset: 73 gelabelte Tickets
- Ausgewertet: 73
- Lauf-Tag: `v4`
- Modell: `claude-haiku-4-5-20251001`
- Lauf: 2026-09-22 19:51:57, 1 Worker

## Category

**Accuracy: 83.6%** (61/73)

```
  (Zeile = Gold, Spalte = Prediction)

                               bill             tech             acct             feat            other   Summe
  billing                        10                .                1                .                2      13
  technical                       .               15                .                .                1      16
  account                         .                .               10                1                .      11
  feature-request                 .                1                1               16                1      19
  other                           2                1                .                1               10      14
  Summe                          12               17               12               18               14      73
```

| Klasse | Support | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| billing | 13 | 0.83 | 0.77 | 0.80 |
| technical | 16 | 0.88 | 0.94 | 0.91 |
| account | 11 | 0.83 | 0.91 | 0.87 |
| feature-request | 19 | 0.89 | 0.84 | 0.86 |
| other | 14 | 0.71 | 0.71 | 0.71 |

Macro-F1: **0.832**

Haeufigste Verwechslungen (Gold -> Prediction):

- `other` -> `billing`: 2x  (Tickets 19, 72)
- `billing` -> `other`: 2x  (Tickets 26, 35)
- `billing` -> `account`: 1x  (Tickets 10)
- `other` -> `technical`: 1x  (Tickets 31)
- `account` -> `feature-request`: 1x  (Tickets 41)

## Urgency

**Accuracy: 79.5%** (58/73)

- **Unterschaetzt** (Modell < Gold): 7 (9.6%) — verschleppte Tickets, das teure Versagen
- **Ueberschaetzt** (Modell > Gold): 8 (11.0%) — unnoetige Eskalation, das laute Versagen

| Abweichung | Anzahl | Tickets |
|---|---:|---|
| 1 Stufe zu niedrig | 7 | 2, 23, 42, 50, 57, 58, 69 |
| korrekt | 58 | — |
| 1 Stufe zu hoch | 6 | 1, 25, 28, 36, 72, 73 |
| 2 Stufen zu hoch | 2 | 30, 44 |

```
  (Zeile = Gold, Spalte = Prediction)

                       low  medium    high   Summe
  low                   34       4       2      40
  medium                 4       9       2      15
  high                   .       3      15      18
  Summe                 38      16      19      73
```

## Sentiment

**Accuracy: 84.9%** (62/73)

```
  (Zeile = Gold, Spalte = Prediction)

                    positive   neutral  negative   Summe
  positive                 2         .         .       2
  neutral                  1        33         3      37
  negative                 .         7        27      34
  Summe                    3        40        30      73
```

Achtung: duenne Klasse(n) im Goldset — positive (n=2). Einzelne Fehler verschieben die Accuracy hier stark.

## Kosten & Latenz

- **Kosten pro 1000 Requests: $2.434** (Ø 2092 Input- / 68 Output-Tokens, $1.00/$5.00 pro Mio)
- **p95-Latenz: 1.41s** (Median 0.88s, Ø 0.96s, max 1.89s)
- Kosten des Laufs: $0.1777
