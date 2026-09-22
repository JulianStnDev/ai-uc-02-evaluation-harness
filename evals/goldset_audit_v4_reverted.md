# Goldset-Audit

> **Zurueckgenommenes Experiment.** Die Prompt-Aenderung, die diesen Lauf erzeugt hat,
> wurde verworfen; classify.py steht wieder auf v3. Der Lauf bleibt als Beleg stehen.
> Begruendung: docs/decisions.md, Eintrag "v4 zurueckgenommen".


- Judge: `claude-sonnet-5` (Klassifikator ist Haiku — bewusst ein anderes
  Modell, damit kein Self-Preference-Bias das Urteil faerbt)
- Geprueft: 73 Tickets x 3 Felder = 219 Einzelurteile
- Lauf: 2026-09-22 19:53:23
- **Widersprueche: 43** (19.6% der Einzelurteile)

> Der Judge aendert keine Labels. Jeder Eintrag unten ist ein Kandidat fuer
> manuelle Nachpruefung — die Entscheidung trifft ein Mensch.

| Feld | Widersprueche |
|---|---:|
| category | 11 |
| urgency | 12 |
| sentiment | 20 |

## category (11)

**#8** — Goldset `feature-request` / Judge `technical`  
> wie archiviere ich ein habit ohne es zu löschen? finde die option nirgends

Der Nutzer sucht eine bestehende, ihm nicht auffindbare Option in der App, was einer Bedienungs-/Auffindbarkeitsfrage zur bestehenden Funktion entspricht, nicht einem Wunsch nach einer neuen Funktion, daher eher technical als feature-request.

**#19** — Goldset `other` / Judge `account`  
> unsubscribe

Ein 'unsubscribe'-Anliegen bezieht sich auf Konto-/Abo-Verwaltung (Abmeldung), was unter account (Konto-Einstellungen) fällt, nicht unter other, da ein konkretes Handlungsanliegen vorliegt.

**#26** — Goldset `billing` / Judge `other`  
> Gibt es Rabatte für Studierende oder Bildungseinrichtungen? Wir sind eine Schule mit ca. 300 Schülern.

Es handelt sich um eine allgemeine Frage zu Rabatten/Preisniveau ohne konkrete Transaktion im eigenen Vertrag, somit fällt dies laut Abgrenzungsregel unter other, nicht billing.

**#31** — Goldset `other` / Judge `technical`  
> kurze frage: zählt der fokus timer weiter wenn ich die app schließe?

Die Frage betrifft das Funktionsverhalten der App (Fokus-Timer), was unter technical fällt, nicht unter other, da kein Presse-, Bewerbungs-, Meinungs- oder Leeranliegen vorliegt.

**#41** — Goldset `account` / Judge `billing`  
> Wie viele Geräte kann ich mit einem Pro-Abo gleichzeitig nutzen?

Die Frage betrifft die Nutzung des Pro-Abos (Anzahl Geräte), also eine Abo-/Vertragsfrage, nicht Login oder Kontoeinstellungen, daher billing statt account.

**#44** — Goldset `feature-request` / Judge `technical`  
> Ich nutze FocusFlow mit VoiceOver. Die Buttons im Timer-Screen haben keine Labels, ich weiß nicht was ich drücke.

Fehlende Accessibility-Labels für VoiceOver sind ein Fehlverhalten/Mangel der App im Timer-Screen, kein Wunsch nach einer neuen Funktion, daher technical statt feature-request.

**#46** — Goldset `other` / Judge `feature-request`  
> Moin, ein Kollege hat mir eure App empfohlen. Gibt es Team- oder Firmenlizenzen? Wir wären ca. 40 Leute.

Die Anfrage nach Team-/Firmenlizenzen ist ein konkreter Wunsch nach einer neuen (Lizenz-)Funktion/Angebot, kein bloßes Meinungsäußern ohne Handlungsaufforderung, daher feature-request statt other.

**#48** — Goldset `other` / Judge `account`  
> wieso brauch ihr zugriff auf meine kontakte??

Die Frage nach dem Zugriff auf Kontakte betrifft App-Berechtigungen im Zusammenhang mit dem eigenen Konto/den eigenen Daten, ist aber laut Regeln am ehesten der Kategorie account (Konto-Einstellungen/Datenschutz zum eigenen Konto) zuzuordnen, nicht other, da es sich um ein konkretes produktbezogenes Anliegen und nicht um eine reine Meinungsäußerung ohne Handlungsaufforderung handelt.

**#49** — Goldset `feature-request` / Judge `billing`  
> Hi, kann ich mein Abo pausieren? Bin die nächsten 3 Monate im Ausland ohne verlässliches Internet.

Die Frage nach dem Pausieren des eigenen Abos bezieht sich auf eine konkrete Transaktion im eigenen Vertrag des Nutzers, das fällt unter billing, nicht unter einen Wunsch nach einer neuen Funktion.

**#68** — Goldset `other` / Judge `account`  
> Frage zur Datenschutzerklärung: wo genau werden die Daten gespeichert, EU oder US?

Eine Frage zum Speicherort der Daten/Datenschutz bezieht sich auf Konto- bzw. Datenschutzeinstellungen des Nutzers und ist kein reines Presse-, Meinungs- oder Leeranliegen ohne Produktbezug, wie es für 'other' erforderlich wäre.

**#72** — Goldset `other` / Judge `billing`  
> warum kostet das jahresabo 59$ und nicht 59€? ich bin in österreich und zahle dadurch wechselkursgebühren

Es geht um die konkrete Preisgestaltung/Währung des eigenen Abos und daraus resultierende Wechselkursgebühren, also eine konkrete Transaktion im eigenen Vertrag, was laut Regel billing ist, nicht other.

## urgency (12)

**#2** — Goldset `high` / Judge `medium`  
> abo wechsel fehlt geld. von normal auf pro keine geld zurück (anteil!!)

Es wird kein konkret bezifferter, bereits eingetretener Betrag genannt, der falsch/doppelt abgebucht oder nicht anteilig gutgeschrieben wurde, sondern nur allgemein bemängelt, dass der Anteil fehlt, was Bedingung (3) nicht ausreichend erfüllt, und keine der anderen High-Bedingungen greift.

**#11** — Goldset `medium` / Judge `high`  
> keine sync zwischen web und android. auf dem laptop sind 5 habits, auf dem handy nur 3.

Die Sync-Funktion ist laut Regel (2) eine zentrale Funktion, die hier komplett ausfällt (keine Synchronisation zwischen Web und Android), was high statt medium rechtfertigt.

**#13** — Goldset `medium` / Judge `low`  
> Hallo, ich benötige für die letzten 6 Monate Rechnungen mit meiner Firmenanschrift und USt-IdNr. Können Sie mir diese zusenden?

Es handelt sich um eine reine Anfrage nach Rechnungsdokumenten ohne genannte Frist, Funktionsausfall oder finanziellen Schaden, was low statt medium entspricht.

**#23** — Goldset `high` / Judge `medium`  
> Hab von monatlich auf jährlich gewechselt und wurde sofort voll belastet, obwohl der laufende Monat schon bezahlt war. Bitte prüfen.

Es wird zwar eine volle Belastung beim Wechsel beklagt, aber kein konkret bezifferter, bereits fälschlich abgebuchter Betrag oder eine nicht erfolgte Erstattung genannt - es ist unklar ob tatsächlich ein doppelter/falscher Betrag abgebucht wurde, zudem fehlt eine explizite Frist.

**#44** — Goldset `low` / Judge `high`  
> Ich nutze FocusFlow mit VoiceOver. Die Buttons im Timer-Screen haben keine Labels, ich weiß nicht was ich drücke.

Ohne Button-Labels kann der VoiceOver-Nutzer die Kernfunktion Fokus-Timer nicht bedienen, da er nicht erkennen kann was er drückt - das ist ein kompletter Funktionsausfall ohne Workaround.

**#47** — Goldset `high` / Judge `medium`  
> Erstattung bitte. Habe Pro gekauft, aber die Habits bleiben bei 3 begrenzt, also funktioniert es nicht.

Es liegt weder eine explizite Frist, noch ein kompletter Funktionsausfall (die App funktioniert, nur die Habit-Grenze wird nicht erhöht), noch ein bereits bezifferter finanzieller Schaden oder Sicherheitsvorfall vor, daher ist high nicht gerechtfertigt.

**#50** — Goldset `medium` / Judge `low`  
> Die deutsche Übersetzung ist an einigen Stellen falsch. Auf dem Statistik-Screen steht Erfolg wo Serie gemeint ist.

Ein falscher Übersetzungstext ist kein echtes Funktionsproblem und erfüllt keine der medium/high-Bedingungen, es handelt sich um einen kleinen kosmetischen Hinweis ohne akutes Problem.

**#53** — Goldset `high` / Judge `medium`  
> Mein Pro-Abo wurde nicht aktiviert, obwohl die Abbuchung durch ist. Seit 4 Tagen. Ich habe schon zweimal geschrieben und keine Antwort bekommen. Langsam werde ich echt sauer.

Es liegt weder eine explizite Frist, noch ein kompletter Funktionsausfall, noch ein bezifferter finanzieller Schaden (die Abbuchung ist erfolgt, aber kein falscher/doppelter Betrag genannt) noch ein Sicherheitsvorfall vor, daher erfüllt das Ticket keine der high-Bedingungen.

**#58** — Goldset `high` / Judge `medium`  
> Nach dem Google Sign-In lande ich in einem leeren Konto, meine alten Habits sind nicht da. Bin ich versehentlich in einem neuen Account?

Kein vollständiger Funktionsausfall des Logins (der Login funktioniert, es fehlen nur die Daten im Konto), keine Frist, kein bezifferter finanzieller Schaden und kein gemeldeter Sicherheitsvorfall, daher erfüllt dies keine der high-Bedingungen.

**#61** — Goldset `high` / Judge `medium`  
> Sehr geehrte Damen und Herren, seit dem Wechsel auf das Jahresabo (59$) erhalte ich weiterhin die Aufforderung, auf Pro upzugraden. Zudem wurde mir der Restbetrag des Monatsabos nicht gutgeschrieben. ...

Der Restbetrag wird als nicht gutgeschrieben beschrieben, aber es ist kein konkreter, bezifferter Betrag genannt und kein sonstiges high-Kriterium erfüllt, daher medium.

**#64** — Goldset `high` / Judge `medium`  
> hab ausversehen mein konto gelöscht. kann man das rückgängig machen? war 2 jahre drin

Es liegt kein unbefugter Zugriff Dritter oder ein anderer gemeldeter Sicherheitsvorfall vor, sondern eine versehentliche eigene Löschung, und es wird keine explizite Frist genannt, weshalb Bedingung (4) bzw. (1) nicht erfüllt ist.

**#69** — Goldset `medium` / Judge `low`  
> sync dauert manchmal 10 minuten. ist das normal?

Es handelt sich um eine Frage ohne Frist, ohne kompletten Funktionsausfall und ohne finanziellen Schaden, daher sollte urgency low statt medium sein.

## sentiment (20)

**#4** — Goldset `negative` / Judge `neutral`  
> timer läuft nicht weiter wenn ich das handy sperre. iphone 15, ios 18.2. sehr nervig beim lernen

Der Nutzer beschreibt ein störendes Verhalten (Timer stoppt bei Sperrung), aber es handelt sich nicht um eine komplette Blockade der Nutzung oder einen Schaden gemäß den negative-Kriterien, sondern lediglich um Ärger über einen Bug ohne vollständigen Funktionsausfall.

**#7** — Goldset `negative` / Judge `neutral`  
> App stürzt seit dem letzten Update direkt beim Start ab. Android 14, Pixel 7. Habe schon deinstalliert und neu installiert, bringt nichts.

Der Nutzer schildert das Problem sachlich (App-Absturz, Gerätedaten, versuchte Lösung) ohne emotionale Sprache, wiederholten Kontakt oder erkennbare Beeinträchtigung über die technische Störung hinaus, sodass laut Regeln neutral zutrifft; allerdings ist ein kompletter Funktionsausfall (App startet nicht) als 'blockierte Nutzung' explizit als negative-Kriterium genannt, weshalb negative ebenfalls vertretbar ist.

**#10** — Goldset `negative` / Judge `neutral`  
> Ich habe mein Abo im App Store gekündigt, aber in der App steht immer noch Pro aktiv bis 2027. Was gilt denn jetzt?

Der Nutzer stellt eine sachliche Frage zum Status seines Abos ohne Hinweis auf Geldverlust, Datenverlust, Sicherheitsvorfall, blockierte Nutzung oder wiederholten unbeantworteten Kontakt.

**#11** — Goldset `negative` / Judge `neutral`  
> keine sync zwischen web und android. auf dem laptop sind 5 habits, auf dem handy nur 3.

Der Text ist eine rein sachliche Fehlerbeschreibung ohne erkennbare emotionale Beeinträchtigung, wiederholten Kontakt oder Schaden, daher neutral statt negative.

**#15** — Goldset `negative` / Judge `neutral`  
> warum nur 3 habits im free tier? andere apps machen 5. bisschen geizig

Das Ticket ist eine allgemeine Meinungsäußerung/Kritik am Funktionsumfang ohne eigenen Schaden, Datenverlust, Sicherheitsvorfall oder wiederholten unbeantworteten Kontakt, daher greift negative nicht.

**#16** — Goldset `negative` / Judge `neutral`  
> Streak ist weg obwohl ich gestern abgehakt habe. Meine Zeitzone ist UTC+1, vielleicht liegt es daran?

Der Nutzer berichtet sachlich von einem Bug und vermutet eine Ursache, ohne dass ein Geldverlust, Datenverlust, Sicherheitsvorfall, komplette Blockade oder wiederholter unbeantworteter Kontakt vorliegt, daher ist neutral statt negative angemessen.

**#28** — Goldset `negative` / Judge `neutral`  
> Im Statistik-Screen ist der Text sehr hell und auf dem weißen Hintergrund kaum zu lesen, vor allem bei Sonnenlicht auf dem Handy-Display.

Es handelt sich um einen sachlichen Bericht eines Lesbarkeitsproblems ohne Geldverlust, Datenverlust, Sicherheitsvorfall, blockierte Nutzung oder Hinweise auf wiederholten/unbeantworteten Kontakt, daher ist neutral statt negative angemessen.

**#30** — Goldset `neutral` / Judge `negative`  
> zahlung fehlgeschlagen steht da, die karte ist aber gedeckt. visa endet auf 4417

Eine fehlgeschlagene Zahlung trotz gedeckter Karte stellt eine blockierte Nutzung/ein Zahlungsproblem dar, das laut Regeln als negative einzustufen ist, unabhängig vom sachlichen Tonfall.

**#36** — Goldset `negative` / Judge `neutral`  
> habits werden seit heute morgen doppelt angezeigt

Der Text ist eine sachliche Fehlerbeschreibung ohne emotionale Sprache, Schadensmeldung oder Hinweis auf wiederholten/unbeantworteten Kontakt, daher trifft negative nicht zu.

**#40** — Goldset `neutral` / Judge `negative`  
> passwort funktioniert nicht mehr obwohl ich es gerade erst neu gesetzt habe. drei mal probiert, immer falsch

Der Nutzer ist durch den blockierten Login-Zugang erkennbar beeinträchtigt, daher geht negative vor neutral.

**#42** — Goldset `negative` / Judge `neutral`  
> Der Timer klingelt zweimal, einmal nach 25 Minuten und dann nochmal ca. eine Minute später. Kleinigkeit, aber es stört.

Der Nutzer beschreibt eine kleine Störung ('Kleinigkeit, aber es stört') ohne Geldverlust, Datenverlust, Sicherheitsvorfall, blockierte Nutzung oder wiederholten unbeantworteten Kontakt, daher liegt keine erkennbare Beeinträchtigung im Sinne der Regel vor.

**#43** — Goldset `neutral` / Judge `positive`  
> SUPER APP!!! nur der preis ist zu hoch für das was sie kann

Das Ticket enthält explizites Lob ('SUPER APP!!!'), was laut Regel als positive einzustufen ist, nicht als neutral.

**#48** — Goldset `negative` / Judge `neutral`  
> wieso brauch ihr zugriff auf meine kontakte??

Es handelt sich um eine allgemeine Frage zu App-Berechtigungen ohne gemeldeten Sicherheitsvorfall, Schaden oder wiederholten unbeantworteten Kontakt, daher ist neutral statt negative angemessen.

**#50** — Goldset `negative` / Judge `neutral`  
> Die deutsche Übersetzung ist an einigen Stellen falsch. Auf dem Statistik-Screen steht Erfolg wo Serie gemeint ist.

Der Text ist eine sachliche Fehlerbeschreibung ohne Hinweis auf Beeinträchtigung, Schaden oder emotionale Sprache.

**#57** — Goldset `negative` / Judge `neutral`  
> Warum wird mir Werbung für Pro angezeigt obwohl ich Pro habe?

Der Nutzer stellt eine sachliche Frage zu einem Fehlverhalten der App ohne erkennbare Anzeichen von Geldverlust, Datenverlust, Sicherheitsvorfall, blockierter Nutzung oder wiederholtem unbeantwortetem Kontakt.

**#60** — Goldset `negative` / Judge `neutral`  
> Ich kann mich seit gestern nicht mehr einloggen, es kommt immer Fehler 500. Ich muss aber heute unbedingt meine Abgabe tracken.

Der Nutzer schildert einen Login-Ausfall sachlich ohne emotionale Sprache, aber der Login-Ausfall selbst ('blockierte Nutzung') zählt laut Regel bereits als negative Kriterium, daher ist negative sogar vertretbar - hier korrigiere ich fälschlich, da blockierte Nutzung explizit negative rechtfertigt.

**#69** — Goldset `negative` / Judge `neutral`  
> sync dauert manchmal 10 minuten. ist das normal?

Der Nutzer stellt eine sachliche Frage ohne erkennbare Beeinträchtigung, Schaden oder Hinweis auf wiederholten Kontakt, daher ist neutral statt negative angemessen.

**#70** — Goldset `negative` / Judge `neutral`  
> kein login möglich. google sign in dreht sich endlos. android, samsung s22

Der Text ist eine sachliche Fehlerbeschreibung ohne emotionale Sprache, ohne Hinweise auf wiederholten Kontakt oder explizit geschilderte Beeinträchtigung über die reine Fehlermeldung hinaus, auch wenn ein Login-Ausfall vorliegt sollte hier neutral gewählt werden, da kein zusätzliches Negativ-Kriterium wie wiederholter Kontakt oder Ton erkennbar ist.

**#72** — Goldset `negative` / Judge `neutral`  
> warum kostet das jahresabo 59$ und nicht 59€? ich bin in österreich und zahle dadurch wechselkursgebühren

Der Nutzer stellt eine sachliche Frage zur Preisgestaltung ohne bezifferten eingetretenen Schaden, wiederholten Kontakt oder erkennbare Beeinträchtigung, daher ist neutral angemessener als negative.

**#73** — Goldset `negative` / Judge `neutral`  
> Hallo, mir ist aufgefallen dass die App beim Beenden eines Fokus-Blocks manchmal einfach zum Startbildschirm springt, ohne die Session zu speichern. Passiert etwa jede 5. Session. Ich habe ein Video d...

Der Nutzer berichtet sachlich über einen intermittierenden Bug (ca. jede 5. Session), ohne dass eine Kernfunktion komplett blockiert wäre, wiederholten unbeantworteten Kontakt erwähnt wird oder ein Schaden entstanden ist, daher ist neutral treffender als negative.

---

Kosten des Audit-Laufs: $0.7179 (246629 Input- / 22466 Output-Tokens)