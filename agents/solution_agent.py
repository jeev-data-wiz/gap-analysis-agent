from utils.llm_client import call_llm
import json

PROMPT = """
Extract structured engineering decisions.

Return JSON list:
[
  {
    "id": "...",
    "decision": "...",
    "tech": [],
    "limitations": [],
    "type": "planned | deferred | scoped",
    "confidence": 0.0-1.0
  }
]

Transcript:
{transcript}
"""

def extract_solutions(transcripts):
    all_solutions = []
    for t in transcripts:
        response = call_llm(PROMPT.format(transcript=t))

        try:
            parsed = json.loads(response)
            all_solutions.extend(parsed)
        except:
            print("Failed parsing solutions")

    return all_solutions
