from utils.llm_client import call_llm
import json

PROMPT = """
Compare requirement and solution.

Return:
{
  "type": "unaddressed | scope_mismatch | implicit_assumption | ambiguity | none",
  "description": "...",
  "suggested_action": "...",
  "confidence": 0.0-1.0
}

Requirement:
{requirement}

Solution:
{solution}
"""

def analyze_gaps(requirements, solutions):
    gaps = []
    gap_id = 1

    for req in requirements:
        matched = False

        for sol in solutions:
            prompt = PROMPT.format(
                requirement=req["statement"],
                solution=sol["decision"]
            )

            response = call_llm(prompt)

            try:
                result = json.loads(response)

                if result["type"] != "none":
                    gaps.append({
                        "gap_id": f"GAP-{gap_id}",
                        "type": result["type"],
                        "description": result["description"],
                        "requirement_ref": req["id"],
                        "solution_ref": sol["id"],
                        "suggested_action": result["suggested_action"],
                        "confidence": result["confidence"]
                    })
                    gap_id += 1
                    matched = True
            except:
                continue

        if not matched:
            gaps.append({
                "gap_id": f"GAP-{gap_id}",
                "type": "unaddressed",
                "description": "No engineering solution found",
                "requirement_ref": req["id"],
                "solution_ref": None,
                "suggested_action": "Clarify implementation",
                "confidence": 0.85
            })
            gap_id += 1

    return gaps
