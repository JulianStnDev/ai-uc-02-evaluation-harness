# Evaluationsergebnisse

- Goldset: 73 gelabelte Tickets
- Ausgewertet: 73
- Lauf-Tag: `baseline`
- Modell: `claude-haiku-4-5-20251001`
- Lauf: 2026-09-22 15:54:48, 1 Worker

## Category

**Accuracy: 82.2%** (60/73)

```
  (Zeile = Gold, Spalte = Prediction)

                               bill             tech             acct             feat            other   Summe
  billing                        12                .                1                .                .      13
  technical                       .               15                1                .                .      16
  account                         .                .               10                .                1      11
  feature-request                 .                1                1               17                .      19
  other                           2                2                2                2                6      14
  Summe                          14               18               15               19                7      73
```

| Klasse | Support | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| billing | 13 | 0.86 | 0.92 | 0.89 |
| technical | 16 | 0.83 | 0.94 | 0.88 |
| account | 11 | 0.67 | 0.91 | 0.77 |
| feature-request | 19 | 0.89 | 0.89 | 0.89 |
| other | 14 | 0.86 | 0.43 | 0.57 |

Macro-F1: **0.801**

Haeufigste Verwechslungen (Gold -> Prediction):

- `other` -> `feature-request`: 2x  (Tickets 15, 46)
- `other` -> `account`: 2x  (Tickets 19, 48)
- `other` -> `technical`: 2x  (Tickets 24, 31)
- `other` -> `billing`: 2x  (Tickets 43, 72)
- `billing` -> `account`: 1x  (Tickets 10)

## Urgency

**Accuracy: 71.2%** (52/73)

- **Unterschaetzt** (Modell < Gold): 7 (9.6%) — verschleppte Tickets, das teure Versagen
- **Ueberschaetzt** (Modell > Gold): 14 (19.2%) — unnoetige Eskalation, das laute Versagen

| Abweichung | Anzahl | Tickets |
|---|---:|---|
| 1 Stufe zu niedrig | 7 | 2, 23, 42, 47, 50, 58, 61 |
| korrekt | 52 | — |
| 1 Stufe zu hoch | 11 | 18, 24, 25, 28, 29, 30, 32, 35, 39, 48, 72 |
| 2 Stufen zu hoch | 3 | 1, 44, 49 |

```
  (Zeile = Gold, Spalte = Prediction)

                       low  medium    high   Summe
  low                   27      10       3      40
  medium                 2      12       1      15
  high                   .       5      13      18
  Summe                 29      27      17      73
```

## Sentiment

**Accuracy: 68.5%** (50/73)

```
  (Zeile = Gold, Spalte = Prediction)

                    positive   neutral  negative   Summe
  positive                 2         .         .       2
  neutral                  5        27         5      37
  negative                 .        13        21      34
  Summe                    7        40        26      73
```

Achtung: duenne Klasse(n) im Goldset — positive (n=2). Einzelne Fehler verschieben die Accuracy hier stark.

## Kosten & Latenz

- **Kosten pro 1000 Requests: $1.379** (Ø 1036 Input- / 69 Output-Tokens, $1.00/$5.00 pro Mio)
- **p95-Latenz: 1.18s** (Median 0.87s, Ø 0.90s, max 1.37s)
- Kosten des Laufs: $0.1006
