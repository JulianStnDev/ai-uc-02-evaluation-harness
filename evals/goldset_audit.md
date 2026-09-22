# Goldset-Audit

- Judge: `claude-sonnet-5` (Klassifikator ist Haiku — bewusst ein anderes
  Modell, damit kein Self-Preference-Bias das Urteil faerbt)
- Geprueft: 73 Tickets x 3 Felder = 219 Einzelurteile
- Lauf: 2026-09-22 19:36:28
- **Widersprueche: 44** (20.1% der Einzelurteile)

> Der Judge aendert keine Labels. Jeder Eintrag unten ist ein Kandidat fuer
> manuelle Nachpruefung — die Entscheidung trifft ein Mensch.

| Feld | Widersprueche |
|---|---:|
| category | 10 |
| urgency | 16 |
| sentiment | 18 |

## category (10)

**#8** — Goldset `feature-request` / Judge `technical`  
> wie archiviere ich ein habit ohne es zu löschen? finde die option nirgends

Der Nutzer fragt nach einer bestehenden Funktion (Archivieren), die er nicht finden kann - das ist eine Bedienungs-/Auffindbarkeitsfrage zur App, kein Wunsch nach einer neuen Funktion, daher eher technical/Nutzungsproblem statt feature-request.

**#26** — Goldset `billing` / Judge `other`  
> Gibt es Rabatte für Studierende oder Bildungseinrichtungen? Wir sind eine Schule mit ca. 300 Schülern.

Es handelt sich um eine allgemeine Frage zu Rabatten/Preisniveau ohne konkreten eigenen Abrechnungsvorgang, was laut Regel unter other statt billing fällt.

**#31** — Goldset `other` / Judge `technical`  
> kurze frage: zählt der fokus timer weiter wenn ich die app schließe?

Die Frage betrifft das Verhalten einer Kernfunktion (Fokus-Timer) der App, was unter technical fällt, nicht unter other, da es sich nicht um Presse-, Meinungs- oder Testanliegen handelt.

**#41** — Goldset `account` / Judge `billing`  
> Wie viele Geräte kann ich mit einem Pro-Abo gleichzeitig nutzen?

Die Frage betrifft die Nutzung des Pro-Abos (Vertragsdetails) und nicht Login, Passwort oder Konto-Einstellungen, daher gehört sie zu billing statt account.

**#44** — Goldset `feature-request` / Judge `technical`  
> Ich nutze FocusFlow mit VoiceOver. Die Buttons im Timer-Screen haben keine Labels, ich weiß nicht was ich drücke.

Fehlende Accessibility-Labels sind ein Fehlverhalten der App (VoiceOver funktioniert nicht wie erwartet), kein Wunsch nach einer neuen Funktion.

**#46** — Goldset `other` / Judge `feature-request`  
> Moin, ein Kollege hat mir eure App empfohlen. Gibt es Team- oder Firmenlizenzen? Wir wären ca. 40 Leute.

Die Anfrage nach Team- oder Firmenlizenzen ist eine konkrete Anfrage nach einer neuen Funktion/Angebotsform der App, keine reine Meinungsäußerung oder Presse-/Kooperationsanfrage ohne Produktbezug.

**#48** — Goldset `other` / Judge `account`  
> wieso brauch ihr zugriff auf meine kontakte??

Die Frage nach dem Zugriff auf Kontakte betrifft App-Berechtigungen/Datenschutz im Zusammenhang mit dem eigenen Konto, was eher als account-Einstellung bzw. Zugriffsrechte einzuordnen ist als 'other', da kein Presse-, Kooperations- oder reines Meinungsanliegen ohne Handlungsaufforderung vorliegt, sondern eine konkrete Frage zum Produktverhalten.

**#49** — Goldset `feature-request` / Judge `billing`  
> Hi, kann ich mein Abo pausieren? Bin die nächsten 3 Monate im Ausland ohne verlässliches Internet.

Die Anfrage betrifft das Pausieren des eigenen Abos, also einen konkreten Vertrags-/Abrechnungsvorgang, was laut Abgrenzungsregel billing statt feature-request ist.

**#68** — Goldset `other` / Judge `account`  
> Frage zur Datenschutzerklärung: wo genau werden die Daten gespeichert, EU oder US?

Eine Frage zur Datenspeicherung im Rahmen der Datenschutzerklärung betrifft die Verarbeitung persönlicher Nutzerdaten/Kontoinformationen und ist somit eher account zuzuordnen, da sie kein reines Presse-, Meinungs- oder Testanliegen ohne Produktbezug ist; zumindest ist sie kein klarer other-Fall, da ein konkretes Anliegen zum eigenen Konto/Datenverarbeitung vorliegt.

**#72** — Goldset `other` / Judge `billing`  
> warum kostet das jahresabo 59$ und nicht 59€? ich bin in österreich und zahle dadurch wechselkursgebühren

Es geht um die konkrete Abrechnungswährung des eigenen Jahresabos und dadurch entstehende Wechselkursgebühren, also eine konkrete Transaktion im eigenen Vertrag, damit billing statt other.

## urgency (16)

**#11** — Goldset `medium` / Judge `high`  
> keine sync zwischen web und android. auf dem laptop sind 5 habits, auf dem handy nur 3.

Die Sync-Funktion, eine zentrale Funktion, ist laut Regel bei komplettem Ausfall ohne Workaround als high einzustufen, und hier fehlen Habits durch fehlgeschlagene Synchronisation komplett auf einem Gerät.

**#13** — Goldset `medium` / Judge `low`  
> Hallo, ich benötige für die letzten 6 Monate Rechnungen mit meiner Firmenanschrift und USt-IdNr. Können Sie mir diese zusenden?

Es handelt sich um eine reine Anfrage nach Rechnungsdokumenten ohne genannte Frist, ohne Funktionsausfall und ohne eingetretenen finanziellen Schaden, also erfüllt es keine der high- oder medium-Bedingungen.

**#14** — Goldset `high` / Judge `medium`  
> Fremder Login aus Vietnam in meinem Konto, ich hab eine mail von euch bekommen. Was soll ich jetzt tun?? da sind meine ganzen daten drin

Es handelt sich um einen möglichen Sicherheitsvorfall, aber es wird weder eine Frist genannt, noch ist der Zugang zum eigenen Konto verloren (der Nutzer kann sich noch einloggen), noch ist ein bezifferter finanzieller Schaden eingetreten.

**#21** — Goldset `high` / Judge `medium`  
> Guten Tag, ich möchte mein Konto und alle damit verbundenen Daten gemäß Art. 17 DSGVO vollständig löschen lassen. Bitte bestätigen Sie mir die Löschung schriftlich innerhalb der gesetzlichen Frist.

Die "gesetzliche Frist" ist keine vom Nutzer konkret genannte Frist im Sinne der Regel, und es liegt weder ein kompletter Funktionsausfall noch ein bezifferter finanzieller Schaden vor.

**#23** — Goldset `high` / Judge `medium`  
> Hab von monatlich auf jährlich gewechselt und wurde sofort voll belastet, obwohl der laufende Monat schon bezahlt war. Bitte prüfen.

Es wurde kein konkreter, bezifferter falscher Betrag genannt und keine Frist gesetzt, daher erfüllt der Fall nicht Bedingung (3) für high.

**#39** — Goldset `medium` / Judge `low`  
> Ich habe versehentlich das falsche Abo gekauft (jährlich statt monatlich), vor ca. 2 Stunden. Kann ich das noch stornieren?

Es handelt sich um eine Frage zur Stornierungsmöglichkeit ohne genannte Frist, kompletten Funktionsausfall oder bereits eingetretenen bezifferten finanziellen Schaden, daher low statt medium.

**#40** — Goldset `high` / Judge `medium`  
> passwort funktioniert nicht mehr obwohl ich es gerade erst neu gesetzt habe. drei mal probiert, immer falsch

Es wird kein dauerhafter Verlust des Kontozugangs beschrieben, sondern drei fehlgeschlagene Versuche mit einem neu gesetzten Passwort, ohne dass eine Frist oder ein vollständiger, dauerhafter Ausfall genannt wird.

**#44** — Goldset `low` / Judge `high`  
> Ich nutze FocusFlow mit VoiceOver. Die Buttons im Timer-Screen haben keine Labels, ich weiß nicht was ich drücke.

Für einen VoiceOver-Nutzer ist der Fokus-Timer durch die fehlenden Labels faktisch unbenutzbar, da er nicht erkennen kann, welchen Button er drückt - das entspricht dem kompletten Ausfall einer Kernfunktion ohne Workaround.

**#47** — Goldset `high` / Judge `medium`  
> Erstattung bitte. Habe Pro gekauft, aber die Habits bleiben bei 3 begrenzt, also funktioniert es nicht.

Es liegt weder eine genannte Frist, noch ein kompletter Funktionsausfall (die App funktioniert, nur die Habit-Grenze ist zu niedrig) noch ein bereits eingetretener bezifferter finanzieller Schaden vor.

**#50** — Goldset `medium` / Judge `low`  
> Die deutsche Übersetzung ist an einigen Stellen falsch. Auf dem Statistik-Screen steht Erfolg wo Serie gemeint ist.

Es handelt sich um einen kleinen Übersetzungsfehler ohne Fristsetzung, ohne kompletten Funktionsausfall und ohne finanziellen Schaden, also low statt medium.

**#53** — Goldset `high` / Judge `medium`  
> Mein Pro-Abo wurde nicht aktiviert, obwohl die Abbuchung durch ist. Seit 4 Tagen. Ich habe schon zweimal geschrieben und keine Antwort bekommen. Langsam werde ich echt sauer.

Es wird keine Frist genannt, keine Kernfunktion ist komplett unbenutzbar und kein bezifferter finanzieller Schaden ist eingetreten (die Abbuchung erfolgte wie vorgesehen, nur die Aktivierung fehlt), daher erfüllt das Ticket keine der drei high-Bedingungen.

**#57** — Goldset `medium` / Judge `low`  
> Warum wird mir Werbung für Pro angezeigt obwohl ich Pro habe?

Es handelt sich um ein reales, aber nicht schwerwiegendes Problem (fehlerhafte Werbeanzeige trotz Pro-Abo) ohne Frist, ohne kompletten Funktionsausfall einer Kernfunktion und ohne bezifferten finanziellen Schaden, daher eher low/medium statt medium mit dieser Begründung - die Formulierung als reine Frage spricht sogar eher für low.

**#58** — Goldset `high` / Judge `medium`  
> Nach dem Google Sign-In lande ich in einem leeren Konto, meine alten Habits sind nicht da. Bin ich versehentlich in einem neuen Account?

Der Login funktioniert, es fehlen nur die alten Habit-Daten nach Anmeldung in einem falschen/neuen Konto - kein kompletter Funktionsausfall ohne Workaround und keine genannte Frist oder bezifferter finanzieller Schaden.

**#61** — Goldset `high` / Judge `medium`  
> Sehr geehrte Damen und Herren, seit dem Wechsel auf das Jahresabo (59$) erhalte ich weiterhin die Aufforderung, auf Pro upzugraden. Zudem wurde mir der Restbetrag des Monatsabos nicht gutgeschrieben. ...

Es ist kein bezifferter, bereits eingetretener Schaden genannt - der nicht gutgeschriebene Restbetrag wird nicht mit einem konkreten Betrag benannt, und es liegt auch keine Frist oder ein kompletter Funktionsausfall vor.

**#64** — Goldset `high` / Judge `medium`  
> hab ausversehen mein konto gelöscht. kann man das rückgängig machen? war 2 jahre drin

Es wird keine Frist genannt und kein bezifferter finanzieller Schaden erwähnt; ein gelöschtes Konto ist zwar ärgerlich, erfüllt aber nicht die engen high-Kriterien (kein Login-Ausfall im Sinne eines bestehenden, aber nicht funktionierenden Zugangs, sondern eine mögliche Wiederherstellungsanfrage).

**#69** — Goldset `medium` / Judge `low`  
> sync dauert manchmal 10 minuten. ist das normal?

Es handelt sich um eine Frage ohne genanntes akutes Problem, keine Frist, kein kompletter Funktionsausfall und kein bezifferter Schaden, daher low statt medium.

## sentiment (18)

**#4** — Goldset `negative` / Judge `neutral`  
> timer läuft nicht weiter wenn ich das handy sperre. iphone 15, ios 18.2. sehr nervig beim lernen

Das Ticket beschreibt ein störendes Verhalten ('sehr nervig'), aber es liegt keine Beeinträchtigung im Sinne der Regeln vor (kein Geldverlust, Datenverlust, Sicherheitsvorfall, komplette Blockade oder wiederholter/unbeantworteter Kontakt), daher ist neutral treffender als negative.

**#7** — Goldset `negative` / Judge `neutral`  
> App stürzt seit dem letzten Update direkt beim Start ab. Android 14, Pixel 7. Habe schon deinstalliert und neu installiert, bringt nichts.

Der Text ist ein sachlicher Fehlerbericht ohne emotionale Sprache, Geldverlust, Datenverlust, Sicherheitsvorfall oder Hinweis auf wiederholten/unbeantworteten Kontakt, daher entspricht er neutral statt negative.

**#10** — Goldset `negative` / Judge `neutral`  
> Ich habe mein Abo im App Store gekündigt, aber in der App steht immer noch Pro aktiv bis 2027. Was gilt denn jetzt?

Der Nutzer stellt lediglich eine sachliche Frage zum Status seines Abos, ohne Hinweis auf finanziellen Schaden, Datenverlust oder wiederholten unbeantworteten Kontakt.

**#15** — Goldset `negative` / Judge `neutral`  
> warum nur 3 habits im free tier? andere apps machen 5. bisschen geizig

Es handelt sich um eine kritische Meinungsäußerung zum Preisniveau/Funktionsumfang ohne Geldverlust, Datenverlust, blockierte Nutzung oder unbeantworteten Kontakt, daher ist negative hier nicht durch die Regeln gedeckt.

**#16** — Goldset `negative` / Judge `neutral`  
> Streak ist weg obwohl ich gestern abgehakt habe. Meine Zeitzone ist UTC+1, vielleicht liegt es daran?

Der Nutzer beschreibt sachlich einen Bug (verlorener Streak) und stellt eine Vermutung zur Ursache an, ohne Hinweise auf starke Beeinträchtigung, Geldverlust, Datenverlust oder wiederholten unbeantworteten Kontakt, daher ist neutral treffender als negative.

**#28** — Goldset `negative` / Judge `neutral`  
> Im Statistik-Screen ist der Text sehr hell und auf dem weißen Hintergrund kaum zu lesen, vor allem bei Sonnenlicht auf dem Handy-Display.

Es handelt sich um einen sachlichen Bericht eines Lesbarkeitsproblems ohne erkennbare Beeinträchtigung wie Geldverlust, Datenverlust, Sicherheitsvorfall oder blockierte Nutzung, daher ist neutral statt negative angemessen.

**#36** — Goldset `negative` / Judge `neutral`  
> habits werden seit heute morgen doppelt angezeigt

Das Ticket beschreibt einen sachlichen Bugbericht (doppelte Anzeige) ohne Hinweis auf Datenverlust, blockierte Nutzung, Geldschaden oder wiederholten unbeantworteten Kontakt, daher ist neutral statt negative angemessen.

**#40** — Goldset `neutral` / Judge `negative`  
> passwort funktioniert nicht mehr obwohl ich es gerade erst neu gesetzt habe. drei mal probiert, immer falsch

Der Nutzer ist durch die blockierte Nutzung (Login funktioniert trotz mehrfacher Versuche nicht) erkennbar beeinträchtigt, was laut Regel als negative einzustufen ist, unabhängig vom ruhigen Tonfall.

**#42** — Goldset `negative` / Judge `neutral`  
> Der Timer klingelt zweimal, einmal nach 25 Minuten und dann nochmal ca. eine Minute später. Kleinigkeit, aber es stört.

Der Nutzer beschreibt selbst eine Kleinigkeit, die zwar stört, aber keine Beeinträchtigung, Schädigung oder blockierte Nutzung darstellt, daher ist neutral treffender als negative.

**#43** — Goldset `neutral` / Judge `positive`  
> SUPER APP!!! nur der preis ist zu hoch für das was sie kann

Das Ticket enthält deutliches Lob ('SUPER APP!!!'), was laut Regel als positive einzustufen ist, nicht neutral.

**#48** — Goldset `negative` / Judge `neutral`  
> wieso brauch ihr zugriff auf meine kontakte??

Die Nachricht ist eine kritische, aber sachliche Nachfrage ohne erkennbaren Geldverlust, Datenverlust, Sicherheitsvorfall oder blockierte Nutzung, daher erfüllt sie nicht die engen Kriterien für negative.

**#50** — Goldset `negative` / Judge `neutral`  
> Die deutsche Übersetzung ist an einigen Stellen falsch. Auf dem Statistik-Screen steht Erfolg wo Serie gemeint ist.

Der Nutzer meldet sachlich einen Übersetzungsfehler ohne erkennbare Beeinträchtigung, Schaden oder emotionale Sprache, was neutral statt negative entspricht.

**#57** — Goldset `negative` / Judge `neutral`  
> Warum wird mir Werbung für Pro angezeigt obwohl ich Pro habe?

Der Text ist eine sachliche Frage ohne Hinweise auf Geldverlust, Datenverlust, Sicherheitsvorfall, blockierte Nutzung oder wiederholten unbeantworteten Kontakt, daher ist neutral statt negative angemessen.

**#60** — Goldset `negative` / Judge `neutral`  
> Ich kann mich seit gestern nicht mehr einloggen, es kommt immer Fehler 500. Ich muss aber heute unbedingt meine Abgabe tracken.

Der Text beschreibt sachlich ein Login-Problem ohne Hinweise auf Geldverlust, Datenverlust, Sicherheitsvorfall oder wiederholten/unbeantworteten Kontakt, daher ist neutral statt negative angemessen.

**#69** — Goldset `negative` / Judge `neutral`  
> sync dauert manchmal 10 minuten. ist das normal?

Der Text ist eine sachliche Frage ohne Hinweis auf Beeinträchtigung, Schaden oder wiederholten unbeantworteten Kontakt, daher neutral statt negative.

**#70** — Goldset `negative` / Judge `neutral`  
> kein login möglich. google sign in dreht sich endlos. android, samsung s22

Das Ticket ist eine rein sachliche Fehlerbeschreibung ohne Hinweise auf finanziellen Schaden, Datenverlust, Sicherheitsvorfall oder wiederholten/unbeantworteten Kontakt, daher ist neutral statt negative angemessen.

**#72** — Goldset `negative` / Judge `neutral`  
> warum kostet das jahresabo 59$ und nicht 59€? ich bin in österreich und zahle dadurch wechselkursgebühren

Es handelt sich um eine sachliche Nachfrage zur Währung ohne eingetretenen Geldverlust, falsche Abbuchung oder sonstige Beeinträchtigung im Sinne der Regeln, daher neutral statt negative.

**#73** — Goldset `negative` / Judge `neutral`  
> Hallo, mir ist aufgefallen dass die App beim Beenden eines Fokus-Blocks manchmal einfach zum Startbildschirm springt, ohne die Session zu speichern. Passiert etwa jede 5. Session. Ich habe ein Video d...

Der Nutzer berichtet sachlich einen Bug (Session wird nicht gespeichert, tritt bei jeder 5. Session auf) ohne emotionale Sprache, Geldverlust, Datenverlust oder Hinweis auf wiederholten unbeantworteten Kontakt, daher neutral statt negative.

---

Kosten des Audit-Laufs: $0.6811 (227649 Input- / 22579 Output-Tokens)