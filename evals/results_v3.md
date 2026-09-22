# Evaluationsergebnisse

- Goldset: 73 gelabelte Tickets
- Ausgewertet: 73
- Lauf-Tag: `v3`
- Modell: `claude-haiku-4-5-20251001`
- Lauf: 2026-09-22 16:35:28, 1 Worker

## Category

**Accuracy: 89.0%** (65/73)

```
  (Zeile = Gold, Spalte = Prediction)

                               bill             tech             acct             feat            other   Summe
  billing                        11                .                .                .                2      13
  technical                       .               15                .                .                1      16
  account                         .                .               10                .                1      11
  feature-request                 .                1                1               17                .      19
  other                           1                1                .                .               12      14
  Summe                          12               17               11               17               16      73
```

| Klasse | Support | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| billing | 13 | 0.92 | 0.85 | 0.88 |
| technical | 16 | 0.88 | 0.94 | 0.91 |
| account | 11 | 0.91 | 0.91 | 0.91 |
| feature-request | 19 | 1.00 | 0.89 | 0.94 |
| other | 14 | 0.75 | 0.86 | 0.80 |

Macro-F1: **0.889**

Haeufigste Verwechslungen (Gold -> Prediction):

- `billing` -> `other`: 2x  (Tickets 26, 35)
- `other` -> `billing`: 1x  (Tickets 19)
- `other` -> `technical`: 1x  (Tickets 31)
- `account` -> `other`: 1x  (Tickets 41)
- `feature-request` -> `technical`: 1x  (Tickets 44)

## Urgency

**Accuracy: 79.5%** (58/73)

- **Unterschaetzt** (Modell < Gold): 8 (11.0%) — verschleppte Tickets, das teure Versagen
- **Ueberschaetzt** (Modell > Gold): 7 (9.6%) — unnoetige Eskalation, das laute Versagen

| Abweichung | Anzahl | Tickets |
|---|---:|---|
| 1 Stufe zu niedrig | 8 | 13, 23, 40, 47, 50, 57, 58, 69 |
| korrekt | 58 | — |
| 1 Stufe zu hoch | 5 | 1, 19, 25, 28, 72 |
| 2 Stufen zu hoch | 2 | 30, 44 |

```
  (Zeile = Gold, Spalte = Prediction)

                       low  medium    high   Summe
  low                   33       5       2      40
  medium                 4      11       .      15
  high                   .       4      14      18
  Summe                 37      20      16      73
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

- **Kosten pro 1000 Requests: $2.228** (Ø 1886 Input- / 68 Output-Tokens, $1.00/$5.00 pro Mio)
- **p95-Latenz: 1.90s** (Median 0.92s, Ø 1.04s, max 7.03s)
- Kosten des Laufs: $0.1627
