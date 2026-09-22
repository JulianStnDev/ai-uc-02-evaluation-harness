"""Klassifikator aus ai-uc-01-ticket-classification.

Unveraendert uebernommen (Tool-Schema, Enum-Beschreibungen, Prompt, Modell) —
UC2 soll genau das messen, was UC1 gebaut hat. Aenderungen hier muessen zurueck
nach UC1 gespiegelt werden, sonst misst der Harness einen Stand, den es nicht gibt.

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
                "description": "billing = Rechnungen/Zahlungen. technical = Bugs, Abstürze, Fehlverhalten der App (nicht login-bezogen). account = Login, Passwort, Zugangsdaten, Konto-Einstellungen. feature-request = Wünsche für neue Funktionen. other = alles andere."
            },
            "urgency": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "high = NUR wenn mindestens eines zutrifft: (1) eine explizite Zeitangabe oder Frist wird genannt, oder (2) eine Kernfunktion ist komplett unbenutzbar ohne Workaround. medium = ein reales Problem, aber ohne genannte Frist und ohne kompletten Funktionsausfall. low = Frage, Wunsch oder kein akutes Problem. Der emotionale Tonfall hat KEINEN Einfluss auf diese Einstufung."
            },
            "sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "negative"],
                "description": "positive = Lob/Dank. neutral = sachlicher Bericht ohne emotionale Sprache. negative = explizite Frustration/Ärger in der Formulierung."
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
