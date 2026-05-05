from utils.llm_client import call_llm
from utils.embedding_client import get_embedding
from utils.vector_store import VectorStore
import json

PROMPT = """
You are a senior technical product reviewer.

Compare requirement and solution carefully.

Classify gap:
- unaddressed
- scope_mismatch
- implicit_assumption
- ambiguity
- none

Be strict. Avoid false positives.

Requirement:
{requirement}

Solution:
{solution}

Return JSON.
"""

def analyze_gaps(requirements, solutions):
    gaps = []
    gap_id = 1

    # Build vector store for solutions
    dim = len(get_embedding("test"))
    store = VectorStore(dim)

    for sol in solutions:
        emb = get_embedding(sol["decision"])
        store.add(emb, sol)

    for req in requirements:
        req_emb = get_embedding(req["statement"])

        # 🔍 Retrieve top-k relevant solutions
        candidates = store.search(req_emb, k=3)

        matched = False

        for sol in candidates:
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
                        "confidence": result.get("confidence", 0.9)
                    })
                    gap_id += 1
                    matched = True

            except:
                continue

        # If no relevant solution found
        if not matched:
            gaps.append({
                "gap_id": f"GAP-{gap_id}",
                "type": "unaddressed",
                "description": "No relevant engineering solution found",
                "requirement_ref": req["id"],
                "solution_ref": None,
                "suggested_action": "Clarify implementation",
                "confidence": 0.85
            })
            gap_id += 1

    return gaps
