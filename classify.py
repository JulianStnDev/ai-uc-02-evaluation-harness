"""Klassifikator, urspruenglich aus ai-uc-01-ticket-classification — hier v2.

v1 war byte-identisch mit UC1 und diente als Baseline (n=73: 82.2% Category-
Accuracy, Urgency 71.2%, Sentiment 68.5%, siehe evals/results_baseline.md).

v2 aendert drei Enum-Beschreibungen, sonst nichts (Modell, Prompt, Tool-Aufruf
unveraendert):
  - category/other:   positive Definition statt Restkategorie (Recall war 0.43)
  - urgency/(1):      Frist zur Problemloesung statt beliebigem Zeitbezug
  - sentiment/negative: risikobasiert statt tonfallbasiert

UC1 bleibt auf dem alten Stand — Begruendung in docs/decisions.md (2026-09-22,
"classify.py entkoppelt sich von UC1").

Der __main__-Block aus UC1 (Demo-Lauf ueber sample_tickets.jsonl, Kosten/Latenz
ueber n=6) ist bewusst nicht mitkopiert: Kosten und Latenz rechnet score.py ueber
das volle Goldset.
"""
import os, json, time
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

CLASSIFY_TOOL = {
    "name": "classify_ticket",
    "description": "Klassifiziert ein Support-Ticket",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["billing", "technical", "account", "feature-request", "other"],
                "description": "billing = Rechnungen/Zahlungen. technical = Bugs, Abstürze, Fehlverhalten der App (nicht login-bezogen). account = Login, Passwort, Zugangsdaten, Konto-Einstellungen. feature-request = Wünsche für neue Funktionen. other = Anliegen, die kein Produktproblem und keinen Funktionswunsch enthalten: Presse-, Medien- und Kooperationsanfragen, Bewerbungen, reine Meinungsäußerungen ohne konkrete Handlungsaufforderung (Lob, Kritik am Preis oder am Produkt allgemein), Test- und Leernachrichten ohne erkennbares Anliegen. other ist eine eigenständige Kategorie mit eigenen Merkmalen, kein Auffangbecken — wähle sie aktiv, wenn diese Merkmale zutreffen, auch wenn eine andere Kategorie thematisch streifbar wäre."
            },
            "urgency": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "high = NUR wenn mindestens eines zutrifft: (1) es wird eine Frist genannt, bis zu der das Problem gelöst sein muss, oder (2) eine Kernfunktion ist komplett unbenutzbar ohne Workaround. Ein bloßer Zeitbezug im Text ist KEINE Frist — wie lange ein Problem schon besteht, wie oft der Nutzer schon geschrieben hat, oder ab wann er verreist/im Ausland ist, erfüllt Bedingung (1) nicht. medium = ein reales Problem, aber ohne genannte Frist und ohne kompletten Funktionsausfall. low = Frage, Wunsch oder kein akutes Problem. Der emotionale Tonfall hat KEINEN Einfluss auf diese Einstufung."
            },
            "sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "negative"],
                "description": "positive = Lob/Dank. neutral = sachlicher Bericht ohne emotionale Sprache. negative = der Nutzer ist erkennbar beeinträchtigt oder geschädigt — der Tonfall ist dafür NICHT ausschlaggebend, eine ruhig formulierte Schadensmeldung zählt genauso wie eine wütende. Dazu zählen: Geldverlust oder falsche Abbuchung, Datenverlust, Sicherheitsvorfall, blockierte oder defekte Nutzung, sowie Hinweise auf wiederholten oder unbeantworteten Kontakt (z.B. 'schon mehrfach geschrieben', 'immer noch keine Antwort', 'seit Tagen keine Reaktion'). Trifft das zu, geht negative der Einstufung neutral vor."
            }
        },
        "required": ["category", "urgency", "sentiment"]
    }
}

def classify(ticket_text):
    start = time.perf_counter()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        tools=[CLASSIFY_TOOL],
        tool_choice={"type": "tool", "name": "classify_ticket"},
        messages=[{"role": "user", "content": f"Ticket: {ticket_text}"}]
    )
    latency = time.perf_counter() - start
    tool_call = next(b for b in response.content if b.type == "tool_use")
    return tool_call.input, latency, response.usage.input_tokens, response.usage.output_tokens
