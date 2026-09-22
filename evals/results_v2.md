# Evaluationsergebnisse

- Goldset: 73 gelabelte Tickets
- Ausgewertet: 73
- Lauf-Tag: `v2`
- Modell: `claude-haiku-4-5-20251001`
- Lauf: 2026-09-22 16:18:52, 1 Worker

## Category

**Accuracy: 86.3%** (63/73)

```
  (Zeile = Gold, Spalte = Prediction)

                               bill             tech             acct             feat            other   Summe
  billing                        10                .                1                1                1      13
  technical                       .               15                .                .                1      16
  account                         .                .               10                1                .      11
  feature-request                 .                1                1               17                .      19
  other                           1                .                1                1               11      14
  Summe                          11               16               13               20               13      73
```

| Klasse | Support | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| billing | 13 | 0.91 | 0.77 | 0.83 |
| technical | 16 | 0.94 | 0.94 | 0.94 |
| account | 11 | 0.77 | 0.91 | 0.83 |
| feature-request | 19 | 0.85 | 0.89 | 0.87 |
| other | 14 | 0.85 | 0.79 | 0.81 |

Macro-F1: **0.858**

Haeufigste Verwechslungen (Gold -> Prediction):

- `billing` -> `account`: 1x  (Tickets 10)
- `other` -> `account`: 1x  (Tickets 19)
- `billing` -> `feature-request`: 1x  (Tickets 26)
- `billing` -> `other`: 1x  (Tickets 35)
- `account` -> `feature-request`: 1x  (Tickets 41)

## Urgency

**Accuracy: 68.5%** (50/73)

- **Unterschaetzt** (Modell < Gold): 14 (19.2%) — verschleppte Tickets, das teure Versagen
- **Ueberschaetzt** (Modell > Gold): 9 (12.3%) — unnoetige Eskalation, das laute Versagen

| Abweichung | Anzahl | Tickets |
|---|---:|---|
| 1 Stufe zu niedrig | 14 | 2, 3, 7, 13, 23, 40, 42, 47, 50, 57, 58, 61, 64, 69 |
| korrekt | 50 | — |
| 1 Stufe zu hoch | 8 | 1, 25, 28, 30, 35, 48, 49, 72 |
| 2 Stufen zu hoch | 1 | 44 |

```
  (Zeile = Gold, Spalte = Prediction)

                       low  medium    high   Summe
  low                   31       8       1      40
  medium                 5      10       .      15
  high                   .       9       9      18
  Summe                 36      27      10      73
```

## Sentiment

**Accuracy: 86.3%** (63/73)

```
  (Zeile = Gold, Spalte = Prediction)

                    positive   neutral  negative   Summe
  positive                 2         .         .       2
  neutral                  1        34         2      37
  negative                 .         7        27      34
  Summe                    3        41        29      73
```

Achtung: duenne Klasse(n) im Goldset — positive (n=2). Einzelne Fehler verschieben die Accuracy hier stark.

## Kosten & Latenz

- **Kosten pro 1000 Requests: $1.856** (Ø 1513 Input- / 69 Output-Tokens, $1.00/$5.00 pro Mio)
- **p95-Latenz: 1.13s** (Median 0.90s, Ø 0.91s, max 1.42s)
- Kosten des Laufs: $0.1355
