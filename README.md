Architecture Overview
This system utilizes a decoupled multi-agent pipeline to bridge the communication gap between business stakeholders and engineering teams. By breaking the "fuzzy" problem into distinct stages, we ensure high reasoning density and minimize context dilution.  

Pipeline Stages
Requirements Extraction Agent (Task 1): Processes informal business transcripts. It uses a "chain-of-thought" prompting strategy to distinguish between "must-haves" and "nice-to-haves" , outputting a schema-validated JSON.  


Solution Extraction Agent (Task 2): Analyzes engineering discussions to map planned implementations, specifically looking for deferred items or scope limitations.  


Gap Analysis Agent (Task 3): A specialized reasoning agent that performs cross-reference analysis. It doesn't just look for missing items; it identifies semantic mismatches (e.g., 24 months vs. 12 months) and unspoken assumptions.  


Orchestration Layer (Task 4): A CLI wrapper that handles directory-wide processing and ensures graceful error handling for malformed transcripts.  


Design Rationale & LLM Reasoning
Multi-Agent Chain preferred over a Single Prompt

A single-call approach often suffers from "lost in the middle" phenomena where the LLM misses nuanced gaps in long transcripts.  

Separation of Concerns: Each agent has a specific "persona" and system prompt, reducing the likelihood of the LLM confusing a business "ask" with an engineering "decision".  

Structured Traceability: Every gap is linked back to a specific requirement_ref and solution_ref, allowing users to verify the agent's logic.  

Model Choice: GPT-4o / Claude 3.5 Sonnet

Reasoning: High-level reasoning is required to identify "implicit assumptions".  

Tool Use: Leveraging structured outputs (JSON mode) ensures that the output of Task 1 is programmatically consumable by Task 3 without parsing errors. 

Setup & Execution
Prerequisites: Python 3.10+   

Clone & Install:

Bash
git clone <repo-link>
pip install -r requirements.txt
Environment Variables:
Create a .env file in the root and add your API key:  

Plaintext
OPENAI_API_KEY=your_key_here
Run the Pipeline:

Bash
python main.py --business ./transcripts/business --engineering ./transcripts/engineering --output report.json

Known Limitations & Honest Critique
Context Window Limits: While the current system handles individual transcript pairs well, it does not yet perform "global" reasoning across 20+ separate meetings.  

Simple Heuristics: Gap identification relies on LLM semantic reasoning; it does not currently use a RAG/Vector database to find historical contradictions.  

Hallucination Risk: In extremely messy transcripts, the agent may occasionally interpret a "question" as a "requirement".  

Future Roadmap
Confidence Scoring: Implement a self-reflection loop where a "Critic Agent" assigns a 1-5 confidence score to each flagged gap.  

Semantic Search: Integrate a vector store (like ChromaDB) to track requirement evolution across multiple months of transcripts.

Interactive CLI: Allow the user to "chat" with the gap report to ask follow-up questions about specific implementation risks.
